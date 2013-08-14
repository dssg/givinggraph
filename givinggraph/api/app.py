'''
Set of RESTful endpoints to query the giving database.  See README.md for
documentation.
'''
# FIXME: Fail gracefully on no results.


import json

from flask import Flask

from givinggraph.models import DBSession, Nonprofit, Company, News_Article, Nonprofits_Similarity_By_Description, Nonprofits_Similarity_By_Tweets
from givinggraph.analysis import sector


app = Flask(__name__)


def result2json(result):
    print result.__dict__
    return json.dumps(dict([(k, v) for k, v in result.__dict__.iteritems() if not k.startswith('_')]))


@app.route('/nonprofit/ein/<ein_id>')
def by_ein(ein_id):
    """Lookup nonprofit by EIN."""
    return result2json(DBSession.query(Nonprofit).filter(Nonprofit.ein == ein_id).first())


@app.route('/nonprofit/id/<nonprofit_id>')
def by_id(nonprofit_id):
    """Lookup nonprofit by our internal id."""
    return result2json(DBSession.query(Nonprofit).filter(Nonprofit.nonprofits_id == nonprofit_id).first())


@app.route('/ntee/<ntee_code>')
def by_ntee(ntee_code):
    """Compute aggregate statistics for this NTEE code."""
    return json.dumps(sector.sector_stats(ntee_code))


if __name__ == '__main__':
    app.run(debug=True)
