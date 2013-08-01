import givinggraph.guidestar.search
import givinggraph.news.searcher as news_searcher
import givinggraph.news.parser as news_parser
import givinggraph.twitter.users
import givinggraph.yahoo.search
from givinggraph.models import DBSession, Nonprofit, Company, News_Article


def add_nonprofit_info_to_db(ein):
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


def update_nonprofit_twitter_name(nonprofits_id):
    nonprofit = DBSession.query(Nonprofit).get(nonprofits_id)
    twitter_url = givinggraph.yahoo.search.get_search_results('twitter ' + nonprofit.name)[0]
    twitter_name = None
    if twitter_url[:11] == 'twitter.com':
        twitter_name = twitter_url[12:]
    nonprofit.twitter_name = twitter_name
    DBSession.commit()


def update_null_nonprofit_twitter_ids():
    '''Finds nonprofits for which the Twitter name is not null, but the Twitter user ID is null,
    and gives the Twitter user ID a value.'''
    query = DBSession.query(Nonprofit).filter(Nonprofit.twitter_id is None)
    nonprofits = query.all()
    screen_names = [nonprofit.twitter_name for nonprofit in nonprofits]
    screen_name_to_id_map = givinggraph.twitter.users.get_screen_name_to_id_map(screen_names)
    for nonprofit in nonprofits:
        nonprofit.twitter_id = screen_name_to_id_map[nonprofit.twitter_name]
    DBSession.commit()


def add_news_articles_to_db_for_nonprofit(nonprofit, companies):
    print 'Getting and processing news articles for nonprofit with ID {0}...'.format(nonprofit.nonprofits_id)
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


def add_news_articles_to_db_for_nonprofits():
    print 'Getting companies...'
    companies = DBSession.query(Company).all()
    print 'Done loading companies.'
    for nonprofit in DBSession.query(Nonprofit).all():
        add_news_articles_to_db_for_nonprofit(nonprofit, companies)
