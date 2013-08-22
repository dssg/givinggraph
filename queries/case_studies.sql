select non1.name, non2.name, my_table.*, rel.companies_id as company1, com.name as name1, rel2.companies_id as company2, com2.name as name2 
from(
	select charity1_id, charity2_id, similarity, news.news_articles_id as news1, news2.news_articles_id as news2 from(
	SELECT * 
	FROM giving.nonprofits_similarity_by_description as non
	order by non.similarity desc limit 1000) as sim left join giving.news_articles as news
	on sim.charity1_id = news.nonprofits_id
	left join giving.news_articles as news2
	on sim.charity2_id = news2.nonprofits_id
	where news.news_articles_id is not null or news2.news_articles_id is not null
	) as my_table
left join giving.news_articles_companies_rel as rel on rel.news_articles_id = my_table.news1
left join giving.companies as com on com.companies_id = rel.companies_id
left join giving.news_articles_companies_rel as rel2 on rel2.news_articles_id = my_table.news2
left join giving.companies as com2 on com2.companies_id = rel2.companies_id

left join giving.nonprofits as non1 on non1.nonprofits_id = my_table.charity1_id
left join giving.nonprofits as non2 on non2.nonprofits_id = my_table.charity2_id
