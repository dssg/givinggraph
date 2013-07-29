import time
from causenet.twitter.common import twitter_get


# takes a list of Twitter screen names as input, and returns a dictionary mapping screen names to IDs
def get_screen_name_to_id_map(screen_names):
    base_url = 'https://api.twitter.com/1.1/users/lookup.json'
    screen_name_to_id_map = {}

    # API call accepts 100 users at a time
    start = 0
    end = 100
    first_execution = (len(screen_names) > 0)  # ensures that the while loop executes at least once
    while first_execution or end < len(screen_names):
        first_execution = False
        params = {'screen_name': '%2c'.join(screen_names[start:end])}  # %2c is the encoding for a comma
        start = end
        end = min(end+100, len(screen_names))

        SLEEP_BETWEEN_REQUESTS_SECONDS = 5
        response = twitter_get(base_url, params)
        if response is None or response.json() is None:
            return None  # something went wrong
        else:
            for user in response.json():
                screen_name_to_id_map[user['screen_name']] = user['id_str']
            max_number_of_requests = int(response.headers['X-Rate-Limit-Limit'])
            requests_remaining = int(response.headers['X-Rate-Limit-Remaining'])
            print '{0} of {1} requests left.'.format(requests_remaining, max_number_of_requests)

            if requests_remaining > 0:
                time.sleep(SLEEP_BETWEEN_REQUESTS_SECONDS)
            else:
                reset_time = int(response.headers['X-Rate-Limit-Reset'])
                seconds_until_reset = reset_time - time.gmtime() + 120  # put in a two minute buffer

                print 'Sleeping until the reset window in ' + seconds_until_reset + ' seconds.'
                time.sleep(seconds_until_reset)
    return screen_name_to_id_map


def get_followers(user_id):
    base_url = 'https://api.twitter.com/1.1/followers/ids.json'
    params = {'user_id': user_id, 'count': 5000}
    all_followers = []
    SLEEP_BETWEEN_REQUESTS_SECONDS = 5
    while True:
        response = twitter_get(base_url, params)
        chunk_of_followers = response.json()
        if chunk_of_followers is None:
            return None  # something went wrong
        elif chunk_of_followers['next_cursor'] == 0:
            return all_followers
        else:
            all_followers.extend(chunk_of_followers)
            params['cursor'] = chunk_of_followers['next_cursor']

            max_number_of_requests = int(response.headers['X-Rate-Limit-Limit'])
            requests_remaining = int(response.headers['X-Rate-Limit-Remaining'])
            print '{0} followers retrieved so far. {1} of {2} requests left.'.format(len(all_followers), requests_remaining, max_number_of_requests)

            if requests_remaining > 0:
                time.sleep(SLEEP_BETWEEN_REQUESTS_SECONDS)
            else:
                reset_time = int(response.headers['X-Rate-Limit-Reset'])
                seconds_until_reset = reset_time - time.gmtime() + 120  # put in a two minute buffer

                print 'Sleeping until the reset window in ' + seconds_until_reset + ' seconds.'
                time.sleep(seconds_until_reset)
