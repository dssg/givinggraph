SELECT * 
FROM giving.nonprofits_top_words_tweets as words, giving.nonprofits as non
WHERE non.name = 'XXX' and non.twitter_name = words.twitter_name