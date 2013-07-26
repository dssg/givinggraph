SELECT tweets.* 
FROM giving.nonprofits_tweets as tweets, giving.nonprofits as non
WHERE non.ein = 'XX-XXXXXXX' and non.twitter_name = tweets.twitter_name
ORDER BY tweets.favorite_count DESC
LIMIT 10