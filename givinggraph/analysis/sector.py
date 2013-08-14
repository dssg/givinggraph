""" For each NTEE code, output statustics such as
- average budget
- average age
- network statistics (hub, authority, clustering coeff)

FIXME: add financial stats
"""

from collections import defaultdict

import numpy as np

from givinggraph.models import DBSession, Nonprofit, Nonprofit_Twitter_Attributes


def sector_stats(ntee):
    """
    Return a dict containing average values for various graph metrics for
    nonprofits with this NTEE code.
    """
    results = DBSession.query(Nonprofit).filter(Nonprofit.ntee_code.like(ntee + '%')).all()
    stats = defaultdict(lambda: [])
    for result in [r for r in results if r.twitter_name]:
        nta = DBSession.query(Nonprofit_Twitter_Attributes).filter(Nonprofit_Twitter_Attributes.id == result.twitter_name).first()
        if nta:
            stats['clustering_coefficient'].append(float(nta.clustering_coefficient))
            stats['hub'].append(float(nta.hub))
            stats['authority'].append(float(nta.authority))
    return dict((k, np.mean(v)) for k, v in stats.iteritems())
