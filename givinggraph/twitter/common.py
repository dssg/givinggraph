import causenet.config
import requests


# url should be the base URL ending in .json
# params is a dictionary where the keys and values are strings
# returns json if the response is OK, returns None is the response is not OK
def twitter_get(url, params):
    complete_url = url + '?'
    for key in params:
        complete_url += key + '=' + str(params[key]) + '&'
    complete_url = complete_url.strip('&')

    r = requests.get(complete_url, auth=causenet.config.get_twitter_authentication())

    if r.status_code == 200:
        return r
    else:
        return None
