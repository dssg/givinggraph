SELECT attr.number_of_followers
FROM giving.nonprofit_twitter_attributes as attr, giving.nonprofits as non
WHERE non.nonprofits_id = XXXXX and non.twitter_name = attr.id