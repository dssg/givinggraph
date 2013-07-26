import requests
from .. import config
from collections import namedtuple

Nonprofit = namedtuple('Nonprofit', 'ein name mission city state zip ntee_code guidestar_participation guidestar_url')


# returns Nonprofit namedtuple if the response is OK, returns None is the response is not OK
def get_nonprofit(ein):
    url = 'https://data.guidestar.org/v1/search.json?q=ein:' + ein

    user = config.read_config('guide_star', 'user')
    password = config.read_config('guide_star', 'pass')
    r = requests.get(url, auth=(user, password))

    if r.status_code == 200:
        nonprofit_dict = r.json()['hits'][0]
        name = nonprofit_dict['organization_name']
        mission = nonprofit_dict['mission']
        city = nonprofit_dict['city']
        state = nonprofit_dict['state']
        zip_code = nonprofit_dict['zip']
        ntee_code = nonprofit_dict['nteecode']
        guidestar_participation = nonprofit_dict['participation']
        guidestar_url = ntee_code = nonprofit_dict['public_report']
        return Nonprofit(ein, name, mission, city, state, zip_code, ntee_code, guidestar_participation, guidestar_url)
    else:
        return None
