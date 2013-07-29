import time
from causenet.twitter.common import twitter_get


# takes a Twitter user id (a string) as input and returns all of that user's tweets, going back as far as the API will let you
def get_tweets(user_id, include_retweets):
    base_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    params = {'user_id': user_id, 'include_rts': include_retweets, 'count': 200}
    all_tweets = []
    SLEEP_BETWEEN_REQUESTS_SECONDS = 5
    while True:
        response = twitter_get(base_url, params)
        chunk_of_tweets = response.json()
        if chunk_of_tweets is None:
            return None  # something went wrong
        elif len(chunk_of_tweets) == 0:
            return all_tweets
        else:
            all_tweets.extend(chunk_of_tweets)
            min_id_found = min([tweet['id'] for tweet in chunk_of_tweets])
            params['max_id'] = str(min_id_found-1)  # we want tweets with IDs lower than min_id_found

            max_number_of_requests = int(response.headers['X-Rate-Limit-Limit'])
            requests_remaining = int(response.headers['X-Rate-Limit-Remaining'])
            print '{0} tweets retrieved so far. {1} of {2} requests left.'.format(len(all_tweets), requests_remaining, max_number_of_requests)

            if requests_remaining > 0:
                time.sleep(SLEEP_BETWEEN_REQUESTS_SECONDS)
            else:
                reset_time = int(response.headers['X-Rate-Limit-Reset'])
                seconds_until_reset = reset_time - time.gmtime() + 120  # put in a two minute buffer

                print 'Sleeping until the reset window in ' + seconds_until_reset + ' seconds.'
                time.sleep(seconds_until_reset)
