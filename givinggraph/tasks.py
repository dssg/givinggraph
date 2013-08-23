"""
Uses celery to ingest a new charity. This is a mix of serial and parallel
tasks, so we use celery to do this efficiently.

This depends on a running instance of a rabbitmq messaging server to keep
track of task statuses. This can be launched on our ec2 instance with:
~/rabbitmq/rabbitmq_server-3.1.3/sbin/rabbitmq-server . If you're developing
locally, you'll have to install rabbitmq (e.g., brew install rabbitmq).

For this script to work, you first need to run a celery worker process to
await orders. From the base dir:
$ celery -A givinggraph.tasks worker --loglevel=info

Then, you can call any of the functions below (see main for an example). To
test on a single nonprofit, run

$ python -m givinggraph.tasks

The worker task will print all the log messages. This is useful for seeing the
order in which tasks are actually executed.

FIXME: Add calls to all the other parts of the pipeline (homepages, community detection, etc)
FIXME: The REST api will be the one calling this in the future.
"""
import csv
import givinggraph.analysis.lda as lda
import givinggraph.analysis.similarity as similarity
import givinggraph.guidestar.search
import givinggraph.news.searcher as news_searcher
import givinggraph.news.parser as news_parser
import givinggraph.twitter.tweets
import givinggraph.twitter.users
import givinggraph.yahoo.search
import time
from celery import Celery
from celery import chain, group
from celery.utils.log import get_task_logger
from givinggraph.models import DBSession, Nonprofit, Company, News_Article, Nonprofits_Similarity_By_Description, Nonprofits_Similarity_By_Tweets, Tweet
from sqlalchemy import func, Integer
from sqlalchemy.sql.expression import cast

'This is the extent of the celery configuration!'
celery = Celery('tasks',
                backend='amqp',
                broker='amqp://guest@localhost//')

logger = get_task_logger(__name__)


def add_new_nonprofit(ein):
    if DBSession.query(Nonprofit).filter(Nonprofit.ein == ein).first() is not None:
        return

    # lookup guidestar info before doing anything else.
    nonprofit = add_guidestar_info_to_db(ein)
    if nonprofit is None:
        print 'Guidestar returned nothing for EIN {0}, exiting.'.format(ein)
        return None

    twitter_chain = chain(update_nonprofit_twitter_name.si(nonprofit.nonprofits_id),
                          group(get_tweets_for_nonprofit.si(nonprofit.nonprofits_id),
                                get_followers_for_nonprofit.si(nonprofit.nonprofits_id)))

    logger.debug('Getting companies...')
    companies = DBSession.query(Company).all()
    logger.debug('Companies retrieved.')

    # add_news_articles_to_db_for_nonprofit returns a list of articles, which will get passed as the 2nd argument to add_nonprofit_company_news_article_connections
    # NOTE: Commented out because of synchronization issue: articles passed to add_nonprofit_company_news_article_connections(...) are in the DB, but SQLAlchemy doesn't see them.
    # news_chain = chain(add_news_articles_to_db_for_nonprofit.si(nonprofit.nonprofits_id),
    #                    add_nonprofit_company_news_article_connections.s(companies))
    article_ids = add_news_articles_to_db_for_nonprofit(nonprofit.nonprofits_id)
    add_nonprofit_company_news_article_connections(article_ids, companies)

    #return group(twitter_chain, news_chain).apply_async()
    return group(twitter_chain).apply_async()


@celery.task(name='tasks.perform_aggregate_tasks')
def perform_aggregate_tasks():
    """Several tasks operate over all nonprofits. This function will execute those tasks."""
    tweets_chain = chain(add_similarity_scores_for_nonprofit_tweets.si(),
                         find_communities_for_tweets.si())
    descriptions_chain = chain(add_similarity_scores_for_nonprofit_descriptions.si(),
                               find_communities_for_descriptions.si())
    followers_chain = chain(find_similarity_scores_for_followers.si(),
                            find_communities_for_followers.si())

    twitter_chain = chain(update_null_nonprofit_twitter_ids.si(),
                          group(tweets_chain,
                                followers_chain))

    return group(twitter_chain, descriptions_chain).apply_async()


@celery.task(name='tasks.add_guidestar_info_to_db')
def add_guidestar_info_to_db(ein):
    """Takes the EIN of a nonprofit as input. If the nonprofit is already in the DB, its info is updated.
    If the nonprofit is not in the DB, it is inserted."""
    logger.debug('Inside add_guidestar_info_to_db({0})'.format(ein))

    query = DBSession.query(Nonprofit).filter(Nonprofit.ein == ein)
    nonprofit_db = query.first()
    nonprofit_gs = givinggraph.guidestar.search.get_nonprofit(ein)
    if nonprofit_gs is None:
        return None

    if nonprofit_db is None:
        nonprofit_db = Nonprofit(nonprofit_gs.name,
                                 nonprofit_gs.ein,
                                 nonprofit_gs.ntee_code,
                                 nonprofit_gs.mission,
                                 nonprofit_gs.mission,
                                 None,
                                 None,
                                 nonprofit_gs.city,
                                 nonprofit_gs.state,
                                 nonprofit_gs.zip)
        DBSession.add(nonprofit_db)
    else:
        nonprofit_db.name = nonprofit_gs.name
        nonprofit_db.ntee_code = nonprofit_gs.ntee_code
        nonprofit_db.mission = nonprofit_gs.mission
        nonprofit_db.description = nonprofit_gs.mission
        nonprofit_db.city = nonprofit_gs.city
        nonprofit_db.state = nonprofit_gs.state
        nonprofit_db.ZIP = nonprofit_gs.zip
    DBSession.commit()
    return nonprofit_db


@celery.task(name='tasks.update_nonprofit_twitter_name')
def update_nonprofit_twitter_name(nonprofits_id):
    """Takes the ID of a nonprofit and uses Yahoo to try to find the Twitter name for that nonprofit.
     If found, the nonprofit's entry in the DB is updated."""
    logger.debug('Inside update_nonprofit_twitter_name(nonprofits_id) for nonprofits_id {0}'.format(nonprofits_id))
    nonprofit = DBSession.query(Nonprofit).get(nonprofits_id)

    search_results = givinggraph.yahoo.search.get_search_results('twitter ' + nonprofit.name)
    if len(search_results) == 0:
        return
    twitter_url = search_results[0]
    twitter_url = twitter_url.replace('http://', '').replace('https://', '')
    twitter_name = None

    if twitter_url[:11] == 'twitter.com':
        twitter_name = twitter_url[12:]
    nonprofit.twitter_name = twitter_name
    DBSession.commit()


@celery.task(name='tasks.update_null_nonprofit_twitter_ids')
def update_null_nonprofit_twitter_ids():
    """Finds nonprofits for which the Twitter name is not null, but the Twitter user ID is null,
    and gives the Twitter user ID a value."""
    logger.debug('Inside update_null_nonprofit_twitter_ids()')

    query = DBSession.query(Nonprofit).filter(Nonprofit.twitter_id == None).filter(Nonprofit.twitter_name != None)  # nopep8
    nonprofits = query.all()
    screen_names = [nonprofit.twitter_name for nonprofit in nonprofits]
    screen_name_to_id_map = givinggraph.twitter.users.get_screen_name_to_id_map(screen_names)
    for nonprofit in nonprofits:
        if nonprofit.twitter_name.lower() in screen_name_to_id_map:
            nonprofit.twitter_id = screen_name_to_id_map[nonprofit.twitter_name.lower()]
        else:
            print '"{0}" was not found, the account may have been deleted or the screen name may have changed.'.format(nonprofit.twitter_name)
    DBSession.commit()


@celery.task(name='tasks.get_tweets_for_nonprofit')
def get_tweets_for_nonprofit(nonprofits_id):
    """Retrieve tweets for the given nonprofit and store them in the DB."""
    logger.debug('Inside get_tweets_for_nonprofit(nonprofit) for nonprofits_id {0}'.format(nonprofits_id))
    nonprofit = DBSession.query(Nonprofit).get(nonprofits_id)

    max_tweet = DBSession.query(func.max(cast(Tweet.tweet_id, Integer)).label('max_tweet_id')).filter(Tweet.twitter_name == nonprofit.twitter_name).first()
    if max_tweet is None or max_tweet.max_tweet_id is None:
        max_tweet_id = 1
    else:
        max_tweet_id = max_tweet.max_tweet_id

    tweets = []
    if nonprofit.twitter_id is not None:
        tweets = givinggraph.twitter.tweets.get_tweets_by_id(nonprofit.twitter_id, True, since_id=max_tweet_id)
    elif nonprofit.twitter_name is not None:
        tweets = givinggraph.twitter.tweets.get_tweets_by_name(nonprofit.twitter_name, True, since_id=max_tweet_id)
    else:
        pass

    for tweet in tweets:
        DBSession.add(Tweet(tweet['user']['screen_name'],
                            tweet['id_str'],
                            tweet['created_at'],
                            tweet['text'].encode('utf-8'),
                            tweet['lang'],
                            tweet['retweet_count'],
                            tweet['favorite_count'],
                            ', '.join([mention['id_str'] for mention in tweet['entities']['user_mentions']]),
                            ', '.join([mention['screen_name'] for mention in tweet['entities']['user_mentions']]),
                            ', '.join([hashtag['text'] for hashtag in tweet['entities']['hashtags']]),
                            ', '.join([url['expanded_url'] for url in tweet['entities']['urls']]),
                            tweet['in_reply_to_screen_name'],
                            tweet['in_reply_to_user_id_str'],
                            tweet['in_reply_to_status_id_str']))
    DBSession.commit()


@celery.task(name='tasks.get_followers_for_nonprofit')
def get_followers_for_nonprofit(nonprofits_id):
    """Retrieve followers for the given nonprofit and store them in the DB."""
    logger.debug('Inside get_followers_for_nonprofit(nonprofit) for nonprofits_id {0}'.format(nonprofits_id))
    nonprofit = DBSession.query(Nonprofit).get(nonprofits_id)
    if nonprofit.twitter_id is not None:
        pass
        # follower_ids = givinggraph.twitter.users.get_followers(nonprofit.twitter_id)
        # DBSession.query(Nonprofits_Follower).filter(Nonprofits_Follower.nonprofit_handle == nonprofit.twitter_name).delete()
        # for follower_id in follower_ids:
        #     DBSession.add(Nonprofits_Follower(nonprofit.twitter_name, follower_id))
        # DBSession.commit()
    else:
        pass


@celery.task(name='tasks.find_similarity_scores_for_followers')
def find_similarity_scores_for_followers():
    """Recalculate similarity scores for followers."""
    logger.debug('Inside find_similarity_scores_for_followers()')


@celery.task(name='tasks.find_communities_for_tweets')
def find_communities_for_tweets():
    """Calculate community memberships for all the nonprofits based on their tweets."""
    logger.debug('Inside find_communities_for_tweets()')


@celery.task(name='tasks.find_communities_for_descriptions')
def find_communities_for_descriptions():
    """Calculate community memberships for all the nonprofits based on their descriptions."""
    logger.debug('Inside find_communities_for_descriptions()')


@celery.task(name='tasks.find_communities_for_followers')
def find_communities_for_followers():
    """Calculate community memberships for all the nonprofits based on their followers."""
    logger.debug('Inside find_communities_for_followers()')


@celery.task(name='tasks.add_news_articles_to_db_for_nonprofit')
def add_news_articles_to_db_for_nonprofit(nonprofits_id):
    """Searches the web for news articles related to the nonprofit and stores them in the DB. Returns the IDs of the news articles found."""
    logger.debug('Inside add_news_articles_to_db_for_nonprofit(nonprofit) for nonprofits_id {0}'.format(nonprofits_id))
    nonprofit = DBSession.query(Nonprofit).get(nonprofits_id)

    query = DBSession.query(News_Article).filter(News_Article.nonprofits_id == nonprofits_id)
    already_retrieved_urls = [news_article.url for news_article in query.all()]
    news_articles = []
    for article in news_searcher.find_news_articles(nonprofit.name, urls_to_ignore=already_retrieved_urls):
        news_articles.append(News_Article(nonprofit.nonprofits_id, article.url, article.headline, article.body))
    DBSession.add_all(news_articles)
    DBSession.commit()
    return [news_article.news_articles_id for news_article in news_articles]


@celery.task(name='tasks.add_nonprofit_company_news_article_connections')
def add_nonprofit_company_news_article_connections(article_ids, companies):
    """Takes a list of IDs of news articles and a list of Company objects as input. If any of
    the articles contain a company name, a link is made in the DB between the article and the company."""
    logger.debug('Inside add_nonprofit_company_news_article_connections(news_articles, companies)')
    for article_id in article_ids:
        article = DBSession.query(News_Article).get(article_id)
        if article is None:
            print '***************************'
            print '***************************'
            print article_id
            print '***************************'
            print '***************************'
            time.sleep(180)
        counter = 1
        for company in companies:
            if counter % 100 == 0:
                print 'Processing article {0} for company {1} of {2}...'.format(article_id, counter, len(companies))
            counter += 1
            for mention in news_parser.get_company_mentions_in_text(article.text, company.name.encode('utf-8')):
                if news_parser.contains_supportive_wording(mention):
                    article.companies.append(company)
                    break
    DBSession.commit()


@celery.task(name='tasks.add_news_articles_to_db_for_nonprofits')
def add_news_articles_to_db_for_nonprofits():
    """Look up news articles for every nonprofit in the DB, and store any news articles containing company names."""
    logger.debug('Inside add_news_articles_to_db_for_nonprofits()')

    logger.debug('Getting companies...')
    companies = DBSession.query(Company).all()
    logger.debug('Done loading companies...')
    for nonprofit in DBSession.query(Nonprofit).all():
        articles = add_news_articles_to_db_for_nonprofit(nonprofit)
        add_nonprofit_company_news_article_connections(companies, articles)


@celery.task(name='tasks.add_similarity_scores_for_nonprofit_descriptions')
def add_similarity_scores_for_nonprofit_descriptions():
    """Calculate similarity scores for every pair of nonprofit descriptions and store them in the DB."""
    logger.debug('Inside add_similarity_scores_for_nonprofit_descriptions()')

    nonprofits = DBSession.query(Nonprofit).filter(Nonprofit.description != None).all()  # nopep8
    similarity_matrix = similarity.get_similarity_scores_all_pairs([nonprofit.description for nonprofit in nonprofits])
    DBSession.query(Nonprofits_Similarity_By_Description).delete()
    for m in xrange(len(similarity_matrix) - 1):
        for n in xrange(m + 1, len(similarity_matrix)):
            DBSession.add(Nonprofits_Similarity_By_Description(nonprofits[m].nonprofits_id, nonprofits[n].nonprofits_id, similarity_matrix[m][n]))
    DBSession.commit()


@celery.task(name='tasks.add_similarity_scores_for_nonprofit_tweets')
def add_similarity_scores_for_nonprofit_tweets():
    """Calculate similarity scores for every pair of nonprofit tweets and store them in the DB."""
    logger.debug('Inside add_similarity_scores_for_nonprofit_tweets()')

    tweets = DBSession.query(Tweet.twitter_name, func.group_concat(Tweet.text).label('text')).group_by(Tweet.twitter_name).all()
    similarity_matrix = similarity.get_similarity_scores_all_pairs([tweet.text for tweet in tweets])
    DBSession.query(Nonprofits_Similarity_By_Tweets).delete()
    for m in xrange(len(similarity_matrix) - 1):
        for n in xrange(m + 1, len(similarity_matrix)):
            DBSession.add(Nonprofits_Similarity_By_Tweets(tweets[m].twitter_name, tweets[n].twitter_name, similarity_matrix[m][n]))
    DBSession.commit()


def show_topics_for_tweets():
    """Experimental code for displaying topics generated by topic modeling."""
    twitter_names = [row.twitter_name for row in DBSession.query(Tweet.twitter_name).group_by(Tweet.twitter_name).all()]
    tweets = []
    print 'Retrieving tweets...'
    for tweet_name in twitter_names:
        tweet_text = [row.text for row in DBSession.query(Tweet.text).filter(Tweet.twitter_name == tweet_name).all()]
        tweets.append('\n'.join(tweet_text))

    print 'Getting topics...'
    lda.get_topics(tweets)


if __name__ == '__main__':
    with open('collaborations.csv', 'rb') as collaborations_file:
        reader = csv.reader(collaborations_file)
        next(reader, None)  # skip header row
        for row in reader:
            ein = row[2].strip()
            ein = ein[:2] + '-' + ein[2:]
            add_new_nonprofit(ein)
    #print add_new_nonprofit('52-1693387')  # WWF
