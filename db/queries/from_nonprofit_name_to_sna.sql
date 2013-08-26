SELECT degree, weighted_degree, eccentricity, closeness_centrality, betweenness_centrality,
	modularity_class, authority, clustering_coefficient, number_of_triangles, 
	weighted_clustering_coefficient, strength, eigenvector_centrality
FROM giving.nonprofit_twitter_attributes as attr, giving.nonprofits as non
WHERE non.name = 'XXX' and non.twitter_name = attr.id