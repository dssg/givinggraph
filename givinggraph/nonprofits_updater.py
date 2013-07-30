import givinggraph.guidestar.search
import givinggraph.yahoo.search
from givinggraph.models import DBSession, Nonprofit


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


def update_nonprofit_twitter_info(nonprofits_id):
    nonprofit = DBSession.query(Nonprofit).get(nonprofits_id)
    twitter_url = givinggraph.yahoo.search.get_top_search_result('twitter ' + nonprofit.name)
    twitter_name = None
    if twitter_url[:11] == 'twitter.com':
        twitter_name = twitter_url[12:]
    nonprofit.twitter_name = twitter_name
    DBSession.commit()
