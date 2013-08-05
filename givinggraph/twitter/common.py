import givinggraph.config
import requests
from urllib import urlencode


def twitter_get(url, params):
    """URL should be the base URL ending in .json. params is a dictionary where the keys and values are strings. Returns json if the response is OK, returns None is the response is not OK."""
    complete_url = url + '?' + urlencode(params)
    r = requests.get(complete_url, auth=givinggraph.config.get_twitter_authentication())
    if r.status_code == 200:
        return r
    else:
        return None
