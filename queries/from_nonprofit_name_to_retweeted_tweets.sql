SELECT tweets.* 
FROM giving.nonprofits_tweets as tweets, giving.nonprofits as non
WHERE non.name = 'XXX' and non.twitter_name = tweets.twitter_name
ORDER BY tweets.retweet_count DESC
LIMIT 10