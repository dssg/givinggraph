SELECT attr.number_of_followers
FROM giving.nonprofit_twitter_attributes as attr, giving.nonprofits as non
WHERE non.name = 'XXX' and non.twitter_name = attr.id