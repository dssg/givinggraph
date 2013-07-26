SELECT non2.nonprofits_id, non2.name as charity, weight as similarity
FROM giving.nonprofit_twitter_edges as edges, giving.nonprofits as non, giving.nonprofits as non2
WHERE non.nonprofits_id = XXXXX and non.twitter_name = edges.source and non2.twitter_name = edges.target

UNION

SELECT non2.nonprofits_id, non2.name as charity, weight as similarity
FROM giving.nonprofit_twitter_edges as edges, giving.nonprofits as non, giving.nonprofits as non2
WHERE non.nonprofits_id = XXXXX and non.twitter_name = edges.target and non2.twitter_name = edges.source

ORDER BY similarity DESC
LIMIT 10
	