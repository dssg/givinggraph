SELECT attr.number_of_followers
FROM giving.nonprofit_twitter_attributes as attr, giving.nonprofits as non
WHERE non.ein = 'XX-XXXXXXX' and non.twitter_name = attr.id