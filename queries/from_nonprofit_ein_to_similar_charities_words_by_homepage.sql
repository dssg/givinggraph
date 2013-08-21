SELECT my_table.nonprofits_id, my_table.charity, my_table.similarity, words.* 
FROM (
	SELECT nonpr.nonprofits_id, nonpr.name as charity,  sim.similarity
	FROM giving.nonprofits_similarity_by_homepage as sim, giving.nonprofits as nonpr, giving.nonprofits as nonpr2
	WHERE nonpr2.ein = 'XX-XXXXXXX' 
		and sim.charity1_id = nonpr2.nonprofits_id and sim.charity2_id = nonpr.nonprofits_id 
	
	UNION

	SELECT nonpr.nonprofits_id, nonpr.name as charity, sim.similarity
	FROM giving.nonprofits_similarity_by_homepage as sim, giving.nonprofits as nonpr, giving.nonprofits as nonpr2
	WHERE nonpr2.ein = 'XX-XXXXXXX' 
		and sim.charity2_id = nonpr2.nonprofits_id and sim.charity1_id = nonpr.nonprofits_id 
		
	ORDER BY similarity DESC
	LIMIT 10
) as my_table
JOIN giving.nonprofits_top_words_homepage as words
	on words.nonprofits_id = my_table.nonprofits_id
ORDER BY similarity DESC
