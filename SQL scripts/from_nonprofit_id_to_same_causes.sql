SELECT non.nonprofits_id, non.name, rel.causes_id, causes.name as cause
FROM giving.nonprofits as non, giving.causes_nonprofits_rel as rel, giving.causes as causes
WHERE non.nonprofits_id = rel.nonprofits_id and
	causes.causes_id = rel.causes_id and
	rel.causes_id in (
		SELECT causes_id 
		FROM giving.causes_nonprofits_rel
		WHERE nonprofits_id = XXXXX 
	)
ORDER BY cause