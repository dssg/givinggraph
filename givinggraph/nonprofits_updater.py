import givinggraph.analysis.similarity as similarity
import givinggraph.guidestar.search
import givinggraph.news.searcher as news_searcher
import givinggraph.news.parser as news_parser
import givinggraph.twitter.users
import givinggraph.yahoo.search
from givinggraph.models import DBSession, Nonprofit, Company, News_Article, Nonprofits_Similarity_By_Description


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
    '''Takes the ID of a nonprofit and uses Yahoo to try to find the Twitter name for that nonprofit.
     If found, the nonprofit's entry in the DB is updated.'''
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
    query = DBSession.query(Nonprofit).filter(Nonprofit.twitter_id == None)  # nopep8
    nonprofits = query.all()
    screen_names = [nonprofit.twitter_name for nonprofit in nonprofits]
    screen_name_to_id_map = givinggraph.twitter.users.get_screen_name_to_id_map(screen_names)
    for nonprofit in nonprofits:
        nonprofit.twitter_id = screen_name_to_id_map[nonprofit.twitter_name]
    DBSession.commit()


def add_news_articles_to_db_for_nonprofit(nonprofit, companies):
    '''Takes a Nonprofit object and a list of Company objects as input. Searches the web for
    news articles related to the nonprofit and stores them in the DB. And if any of the articles
    contain a company name, a link is made in the DB between the article and the company.'''
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


def add_similarity_scores_for_nonprofit_descriptions():
    nonprofits = DBSession.query(Nonprofit).filter(Nonprofit.description != None).all()  # nopep8
    similarity_matrix = similarity.get_similarity_scores_all_pairs([nonprofit.description for nonprofit in nonprofits])
    for m in xrange(len(similarity_matrix) - 1):
        for n in xrange(m + 1, len(similarity_matrix)):
            DBSession.add(Nonprofits_Similarity_By_Description(nonprofits[m].nonprofits_id, nonprofits[n].nonprofits_id, similarity_matrix[m][n]))
    DBSession.commit()
