SELECT nonpr.nonprofits_id, nonpr.name as charity, sim.similarity 
FROM giving.nonprofits_similarity_by_homepage as sim, giving.nonprofits as nonpr 
WHERE sim.charity1_id = 11126 and sim.charity2_id = nonpr.nonprofits_id  

UNION

SELECT nonpr.nonprofits_id, nonpr.name as charity, sim.similarity 
FROM giving.nonprofits_similarity_by_homepage as sim, giving.nonprofits as nonpr 
WHERE sim.charity2_id = 11126 and sim.charity1_id = nonpr.nonprofits_id  

ORDER BY similarity DESC
LIMIT 10