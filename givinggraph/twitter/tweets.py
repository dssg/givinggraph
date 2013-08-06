from givinggraph.twitter.common import twitter_get


def get_tweets(user_id, include_retweets):
    """Takes a Twitter user id (a string) as input and returns all of that user's tweets, going back as far as the API will let you."""
    base_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    params = {'user_id': user_id,
              'include_rts': include_retweets,
              'count': 200}
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
