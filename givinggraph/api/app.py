'''
Set of RESTful endpoints to query the giving database.  See README.md for
documentation.
'''
# FIXME: Fail gracefully on no results.


import json

import decimal

from flask import Flask

from flask import request

from givinggraph.models import DBSession, Nonprofit, Company, News_Article, Nonprofits_Similarity_By_Description, Nonprofits_Similarity_By_Tweets
from givinggraph.analysis import sector


app = Flask(__name__)


def result2json(result):
    print result.__dict__
    return json.dumps(dict([(k, v) for k, v in result.__dict__.iteritems() if not k.startswith('_')]))


def procedure_to_json(result):
    items = result.fetchall()
    names = result.keys()
    result.close()
    my_dict = {}
    my_dict['results'] = []
    for i, item in enumerate(items):
        new_dict = {}
        for j, acc in enumerate(item):
            if isinstance(acc, decimal.Decimal):
                new_dict[names[j]] = float(acc)
            else:
                new_dict[names[j]] = acc
        my_dict['results'].append(new_dict)
    return my_dict


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


@app.route('/similarity')
def similarity():
    """Return the most similar nonprofits given a nonprofits and a metric."""
    top = 10 if request.args.get('top') is None else int(request.args.get('top'))
    attr = request.args.get('attr')
    if(attr == 'description'):
        query = 'call  from_nonprofit_id_to_similar_charities_by_description(%d, %d)' % (int(request.args.get('id')), top)
        result = DBSession.execute(query)
        return json.dumps(procedure_to_json(result))
    elif(attr == 'homepage'):
        query = 'call  from_nonprofit_id_to_similar_charities_by_homepage(%d, %d)' % (int(request.args.get('id')), top)
        result = DBSession.execute(query)
        return json.dumps(procedure_to_json(result))
    elif(attr == 'tweets'):
        query = 'call  from_nonprofit_id_to_similar_charities_by_tweets(%d, %d)' % (int(request.args.get('id')), top)
        result = DBSession.execute(query)
        return json.dumps(procedure_to_json(result))
    elif(attr == 'followers'):
        query = 'call  from_nonprofit_id_to_similar_charities_by_followers(%d, %d)' % (int(request.args.get('id')), top)
        result = DBSession.execute(query)
        return json.dumps(procedure_to_json(result))


@app.route('/graph_stats')
def graph_stats():
    """Return the SNA indexes given a nonprofit"""
    query = 'call  from_nonprofit_id_to_sna(%d)' % int(request.args.get('id'))
    result = DBSession.execute(query)
    return json.dumps(procedure_to_json(result))


@app.route('/twitter')
def twitter():
    """Return the SNA indexes given a nonprofit"""
    query = 'call  from_nonprofit_id_to_twitter(%d)' % int(request.args.get('id'))
    result = DBSession.execute(query)
    return json.dumps(procedure_to_json(result))


@app.route('/sector_summary')
def sector_summary():
    """Return the SNA indexes given a nonprofit"""
    query = "call  sector_summary('%s')" % request.args.get('ntee')
    result = DBSession.execute(query)
    return json.dumps(procedure_to_json(result))


if __name__ == '__main__':
    app.run(debug=True)
