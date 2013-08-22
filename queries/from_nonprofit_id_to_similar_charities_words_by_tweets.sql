SELECT my_table.nonprofits_id, my_table.charity, my_table.similarity, words.* 
FROM (
	SELECT nonpr.nonprofits_id, nonpr.name as charity,  sim.similarity , nonpr.twitter_name as twitter_name
	FROM giving.nonprofits_similarity_by_tweets as sim, giving.nonprofits as nonpr, giving.nonprofits as nonpr2
	WHERE nonpr2.nonprofits_id = XXXXX 
		and sim.twitter_name1 = nonpr2.twitter_name and sim.twitter_name2 = nonpr.twitter_name 
 	
	UNION

	SELECT nonpr.nonprofits_id, nonpr.name as charity, sim.similarity, nonpr.twitter_name as twitter_name
	FROM giving.nonprofits_similarity_by_tweets as sim, giving.nonprofits as nonpr, giving.nonprofits as nonpr2
	WHERE nonpr2.nonprofits_id = XXXXX 
		and sim.twitter_name2 = nonpr2.twitter_name and sim.twitter_name1 = nonpr.twitter_name  
	
	ORDER BY similarity DESC
	LIMIT 10
) as my_table
JOIN giving.nonprofits_top_words_tweets as words on words.twitter_name = my_table.twitter_name
ORDER BY similarity DESC
