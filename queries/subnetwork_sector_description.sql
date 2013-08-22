select
 nsbd.charity1_id as Source, nsbd.charity2_id as Target, nsbd.similarity as Weight
from
 giving.nonprofits_similarity_by_description nsbd
 JOIN giving.causes_nonprofits_rel2 rel_first
 JOIN giving.causes_nonprofits_rel2 rel_second
 ON rel_first.nonprofit_id = charity1_id and rel_second.nonprofit_id = charity2_id
where
 rel_first.cause_name = 'Peace' and rel_second.cause_name = 'Peace'
order by
 nsbd.similarity desc