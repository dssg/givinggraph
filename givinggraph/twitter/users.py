from givinggraph.twitter.common import twitter_get


def get_screen_name_to_id_map(screen_names):
    """Takes a list of Twitter screen names as input, and returns a dictionary mapping lower-case screen names to IDs."""
    base_url = 'https://api.twitter.com/1.1/users/lookup.json'
    screen_name_to_id_map = {}

    chunk_size = 100  # API call accepts 100 users at a time
    for i in xrange(0, len(screen_names), chunk_size):
        params = {'screen_name': ','.join(screen_names[i:i + chunk_size])}

        users = twitter_get(base_url, params, 5)
        if users is None:
            return None  # something went wrong
        else:
            for user in users:
                screen_name_to_id_map[user['screen_name'].lower()] = user['id_str']
    return screen_name_to_id_map


def get_followers(user_id):
    """Takes a Twitter user ID as input, and returns that user's followers in the form of a list of Twitter IDs."""
    base_url = 'https://api.twitter.com/1.1/followers/ids.json'
    params = {'user_id': user_id, 'count': 5000}
    all_followers = []
    while True:
        id_info = twitter_get(base_url, params, 60)
        if id_info is None:
            return None  # something went wrong
        elif id_info['next_cursor'] == 0:
            return all_followers
        else:
            all_followers.extend(id_info['ids'])
            params['cursor'] = id_info['next_cursor_str']

            print '{0} followers retrieved so far.'.format(len(all_followers))
