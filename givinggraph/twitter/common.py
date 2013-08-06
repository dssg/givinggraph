import givinggraph.config
import requests
import time
from urllib import urlencode


def twitter_get(url, params, sleep_time_seconds):
    """
    URL should be the base URL ending in .json.
    params is a dictionary where the keys and values are strings.
    sleep_time_seconds is how long the process should sleep for after the request. Should be determined by the Twitter API rate limit.
    Returns json if the response is OK, returns None is the response is not OK.
    """
    complete_url = url + '?' + urlencode(params)
    r = requests.get(complete_url, auth=givinggraph.config.get_twitter_authentication())

    max_number_of_requests = int(r.headers['X-Rate-Limit-Limit'])
    requests_remaining = int(r.headers['X-Rate-Limit-Remaining'])
    print '{0} of {1} requests left.'.format(requests_remaining, max_number_of_requests)

    if requests_remaining > 0:
        time.sleep(sleep_time_seconds)
    else:
        reset_time = int(r.headers['X-Rate-Limit-Reset'])
        seconds_until_reset = reset_time - time.gmtime() + 120  # put in a two minute buffer

        print 'Sleeping until the reset window in ' + seconds_until_reset + ' seconds.'
        time.sleep(seconds_until_reset)

    if r.status_code == 200:
        return r.json()
    else:
        return None
