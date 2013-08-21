SELECT nonpr.nonprofits_id, nonpr.name as charity, sim.similarity 
FROM giving.nonprofits_similarity_by_tweets as sim, giving.nonprofits as nonpr, giving.nonprofits as nonpr2 
WHERE nonpr2.nonprofits_id = XXXXX and sim.twitter_name1 = nonpr2.twitter_name and sim.twitter_name2 = nonpr.twitter_name

UNION

SELECT nonpr.nonprofits_id, nonpr.name as charity, sim.similarity 
FROM giving.nonprofits_similarity_by_tweets as sim, giving.nonprofits as nonpr, giving.nonprofits as nonpr2
WHERE nonpr2.nonprofits_id = XXXXX and sim.twitter_name2 = nonpr2.twitter_name and sim.twitter_name1 = nonpr.twitter_name

ORDER BY similarity DESC
LIMIT 10