from givinggraph.twitter.common import twitter_get


def get_tweets_by_id(user_id, include_retweets, since_id=0):
    """Takes a Twitter user id (a string) as input and returns all of that user's tweets. If since_id is not set, it will go back as far as the API will let you."""
    params = {'user_id': user_id,
              'include_rts': include_retweets,
              'since_id': since_id}
    return __get_tweets(params)


def get_tweets_by_name(screen_name, include_retweets, since_id=0):
    """Takes a Twitter screen name as input and returns all of that user's tweets. If since_id is not set, it will go back as far as the API will let you."""
    params = {'screen_name': screen_name,
              'include_rts': include_retweets,
              'since_id': since_id}
    return __get_tweets(params)


def __get_tweets(params):
    """Takes a Twitter user id (a string) or screen name as input (screen_name takes precedent) and returns all of that user's tweets, going back as far as the API will let you."""
    base_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    params['count'] = 200
    all_tweets = []
    while True:
        chunk_of_tweets = twitter_get(base_url, params, 5)
        if chunk_of_tweets is None:
            return None  # something went wrong
        elif len(chunk_of_tweets) == 0:
            return all_tweets
        else:
            all_tweets.extend(chunk_of_tweets)
            min_id_found = min([tweet['id'] for tweet in chunk_of_tweets])
            params['max_id'] = str(min_id_found - 1)  # we want tweets with IDs lower than min_id_found

            print '{0} tweets retrieved so far.'.format(len(all_tweets))
