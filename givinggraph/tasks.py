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

FIXME: Add calls to all the other parts of the pipeline (news, twitter, etc)
FIXME: The REST api will be the one calling this in the future.
"""

import givinggraph.analysis.similarity as similarity
import givinggraph.guidestar.search
import givinggraph.news.searcher as news_searcher
import givinggraph.news.parser as news_parser
import givinggraph.twitter.users
import givinggraph.yahoo.search
from celery import Celery
from celery import chain, group
from celery.utils.log import get_task_logger
from givinggraph.models import DBSession, Nonprofit, Company, News_Article, Nonprofits_Similarity_By_Description

'This is the extent of the celery configuration!'
celery = Celery('tasks',
                backend='amqp',
                broker='amqp://guest@localhost//')

logger = get_task_logger(__name__)


def process_ein(ein):
    nonprofit = add_guidestar_info_to_db(ein)

    tweets_chain = chain(get_tweets_for_nonprofit.si(nonprofit),
                         find_similarity_scores_for_tweets.si(),
                         find_communities_for_tweets.si())
    descriptions_chain = chain(find_similarity_scores_for_descriptions.si(),
                               find_communities_for_descriptions.si())
    followers_chain = chain(get_followers_for_nonprofit.si(nonprofit),
                            find_similarity_scores_for_followers.si(),
                            find_communities_for_followers.si())

    twitter_chain = chain(update_nonprofit_twitter_name.si(ein),
                          update_null_nonprofit_twitter_ids.si(),
                          group(tweets_chain,
                                followers_chain))

    news_chain = chain(add_news_articles_to_db_for_nonprofits.si())

    # lookup guidestar info before doing anything else.
    return group(twitter_chain, descriptions_chain, news_chain).apply_async()


@celery.task(name='tasks.add_guidestar_info_to_db')
def add_guidestar_info_to_db(ein):
    """Takes the EIN of a nonprofit as input. If the nonprofit is already in the DB, its info is updated.
    If the nonprofit is not in the DB, it is inserted."""
    logger.debug('Inside add_guidestar_info_to_db({0})'.format(ein))

    query = DBSession.query(Nonprofit).filter(Nonprofit.ein == ein)
    nonprofit_db = query.first()
    nonprofit_gs = givinggraph.guidestar.search.get_nonprofit(ein)
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
                                 nonprofit_gs.zip_code)
        DBSession.add(nonprofit_db)
    else:
        nonprofit_db.name = nonprofit_gs.name
        nonprofit_db.ntee_code = nonprofit_gs.ntee_code
        nonprofit_db.mission = nonprofit_gs.mission
        nonprofit_db.description = nonprofit_gs.mission
        nonprofit_db.city = nonprofit_gs.mission
        nonprofit_db.state = nonprofit_gs.mission
        nonprofit_db.ZIP = nonprofit_gs.zip_code
    DBSession.commit()
    return nonprofit_db


@celery.task(name='tasks.update_nonprofit_twitter_name')
def update_nonprofit_twitter_name(nonprofits_id):
    """Takes the ID of a nonprofit and uses Yahoo to try to find the Twitter name for that nonprofit.
     If found, the nonprofit's entry in the DB is updated."""
    logger.debug('Inside update_nonprofit_twitter_name({0})'.format(nonprofits_id))

    nonprofit = DBSession.query(Nonprofit).get(nonprofits_id)
    twitter_url = givinggraph.yahoo.search.get_search_results('twitter ' + nonprofit.name)[0]
    twitter_name = None
    if twitter_url[:11] == 'twitter.com':
        twitter_name = twitter_url[12:]
    nonprofit.twitter_name = twitter_name
    DBSession.commit()


# @celery.task(name='tasks.update_nonprofit_twitter_id')
# def update_nonprofit_twitter_id(nonprofits_id):
#     """Try to update the Twitter user ID for this nonprofit."""
#     nonprofit = DBSession.query(Nonprofit).get(nonprofits_id)
#     if nonprofit.twitter_name is None:
#         return
#     screen_name_to_id_map = givinggraph.twitter.users.get_screen_name_to_id_map([nonprofit.twitter_name])
#     nonprofit.twitter_id = screen_name_to_id_map[nonprofit.twitter_name]
#     DBSession.commit()


@celery.task(name='tasks.update_null_nonprofit_twitter_ids')
def update_null_nonprofit_twitter_ids():
    """Finds nonprofits for which the Twitter name is not null, but the Twitter user ID is null,
    and gives the Twitter user ID a value."""
    logger.debug('Inside update_null_nonprofit_twitter_ids()')

    query = DBSession.query(Nonprofit).filter(Nonprofit.twitter_id == None)  # nopep8
    nonprofits = query.all()
    screen_names = [nonprofit.twitter_name for nonprofit in nonprofits]
    screen_name_to_id_map = givinggraph.twitter.users.get_screen_name_to_id_map(screen_names)
    for nonprofit in nonprofits:
        nonprofit.twitter_id = screen_name_to_id_map[nonprofit.twitter_name]
    DBSession.commit()


@celery.task(name='tasks.get_tweets_for_nonprofit')
def get_tweets_for_nonprofit(nonprofit):
    """Retrieve tweets for the given nonprofit and store them in the DB."""
    logger.debug('Inside get_tweets_for_nonprofit(nonprofit) for nonprofits_id {0}'.format(nonprofit.nonprofits_id))


@celery.task(name='tasks.get_followers_for_nonprofit')
def get_followers_for_nonprofit(nonprofit):
    """Retrieve followers for the given nonprofit and store them in the DB."""
    logger.debug('Inside get_followers_for_nonprofit(nonprofit) for nonprofits_id {0}'.format(nonprofit.nonprofits_id))


@celery.task(name='tasks.find_similarity_scores_for_tweets')
def find_similarity_scores_for_tweets():
    """Recalculate similarity scores for tweets."""
    logger.debug('Inside find_similarity_scores_for_tweets()')


@celery.task(name='tasks.find_similarity_scores_for_descriptions')
def find_similarity_scores_for_descriptions():
    """Recalculate similarity scores for descriptions."""
    logger.debug('Inside find_similarity_scores_for_descriptions()')


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
def add_news_articles_to_db_for_nonprofit(nonprofit, companies):
    """Takes a Nonprofit object and a list of Company objects as input. Searches the web for
    news articles related to the nonprofit and stores them in the DB. And if any of the articles
    contain a company name, a link is made in the DB between the article and the company."""
    logger.debug('Inside add_news_articles_to_db_for_nonprofit(nonprofit, companies) for nonprofits_id {0}'.format(nonprofit.nonprofits_id))

    query = DBSession.query(News_Article).filter(News_Article.nonprofits_id == nonprofit.nonprofits_id)
    already_retrieved_urls = [news_article.url for news_article in query.all()]
    for article in news_searcher.find_news_articles(nonprofit.name, urls_to_ignore=already_retrieved_urls):
        news_article = News_Article(nonprofit.nonprofits_id, article.url, article.headline, article.body)
        DBSession.add(news_article)
        for company in companies:
            for mention in news_parser.get_company_mentions_in_text(article.body, company.name.encode('utf-8')):
                if news_parser.contains_supportive_wording(mention):
                    news_article.companies.append(company)
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
        add_news_articles_to_db_for_nonprofit(nonprofit, companies)


@celery.task(name='tasks.add_similarity_scores_for_nonprofit_descriptions')
def add_similarity_scores_for_nonprofit_descriptions():
    """Calculate similarity scores for every pair of nonprofit descriptions and store them in the DB."""
    logger.debug('Inside add_similarity_scores_for_nonprofit_descriptions()')

    nonprofits = DBSession.query(Nonprofit).filter(Nonprofit.description != None).all()  # nopep8
    similarity_matrix = similarity.get_similarity_scores_all_pairs([nonprofit.description for nonprofit in nonprofits])
    for m in xrange(len(similarity_matrix) - 1):
        for n in xrange(m + 1, len(similarity_matrix)):
            DBSession.add(Nonprofits_Similarity_By_Description(nonprofits[m].nonprofits_id, nonprofits[n].nonprofits_id, similarity_matrix[m][n]))
    DBSession.commit()


if __name__ == '__main__':
    print process_ein('52-1693387')  # WWF
