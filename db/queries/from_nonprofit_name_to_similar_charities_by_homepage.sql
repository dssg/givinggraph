SELECT nonpr.nonprofits_id, nonpr.name as charity, sim.similarity 
FROM giving.nonprofits_similarity_by_homepage as sim, giving.nonprofits as nonpr, giving.nonprofits as nonpr2
WHERE nonpr2.name = 'XXX' and sim.charity2_id = nonpr.nonprofits_id  and sim.charity1_id = nonpr2.nonprofits_id

UNION

SELECT nonpr.nonprofits_id, nonpr.name as charity, sim.similarity 
FROM giving.nonprofits_similarity_by_homepage as sim, giving.nonprofits as nonpr, giving.nonprofits as nonpr2 
WHERE nonpr2.name = 'XXX' and sim.charity1_id = nonpr.nonprofits_id and sim.charity2_id = nonpr2.nonprofits_id 

ORDER BY similarity DESC
LIMIT 10
