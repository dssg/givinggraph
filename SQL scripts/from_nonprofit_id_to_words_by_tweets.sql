SELECT * 
FROM giving.nonprofits_top_words_tweets as words, giving.nonprofits as non
WHERE non.nonprofits_id = XXXXX and non.twitter_name = words.twitter_name