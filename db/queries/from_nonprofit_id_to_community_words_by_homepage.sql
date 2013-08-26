SELECT causes.name,  words.* 
FROM (
	SELECT * 
	FROM giving.nonprofits_communities_by_homepage as com
	WHERE com.nonprofits_id = XXXXX
) as my_table
JOIN giving.nonprofits_communities_by_homepage_words as words
	on my_table.causes_id = words.causes_id and my_table.community = words.community 
LEFT JOIN  giving.causes as causes 	on causes.causes_id = my_table.causes_id