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
    my_dict = {'results': []}
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
    if attr == 'description':
        query = 'call  from_nonprofit_id_to_similar_charities_by_description(%d, %d)' % (int(request.args.get('id')), top)
    elif attr == 'homepage':
        query = 'call  from_nonprofit_id_to_similar_charities_by_homepage(%d, %d)' % (int(request.args.get('id')), top)
    elif attr == 'tweets':
        query = 'call  from_nonprofit_id_to_similar_charities_by_tweets(%d, %d)' % (int(request.args.get('id')), top)
    elif attr == 'followers':
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
    """Return twitter-related information given a nonprofit"""
    query = 'call  from_nonprofit_id_to_twitter(%d)' % int(request.args.get('id'))
    result = DBSession.execute(query)
    return json.dumps(procedure_to_json(result))


@app.route('/sector_summary')
def sector_summary():
    """Return the summary of a given NTEE code"""
    query = "call  sector_summary('%s')" % request.args.get('ntee')
    result = DBSession.execute(query)
    my_dict = procedure_to_json(result)

    nonprofits = my_dict['results']

    result = {
        'avg_closeness_centrality': 0,
        'avg_clustering_coefficient': 0,
        'avg_degree': 0,
        'avg_hubAuth': 0,
        'avg_weighted_degree': 0,
        'avg_eccentricity': 0,
        'avg_clustering_coefficient': 0
    }

    tw_communities = {}
    web_communities = {}
    desc_communities = {}

    for nonprofit in nonprofits:
        result['avg_closeness_centrality'] += nonprofit['closeness_centrality'] / float(len(nonprofits))
        result['avg_clustering_coefficient'] += nonprofit['clustering_coefficient'] / float(len(nonprofits))
        result['avg_degree'] += nonprofit['degree'] / float(len(nonprofits))
        result['avg_hubAuth'] += nonprofit['hubAuth'] / float(len(nonprofits))
        result['avg_weighted_degree'] += nonprofit['weighted_degree'] / float(len(nonprofits))
        result['avg_eccentricity'] += nonprofit['eccentricity'] / float(len(nonprofits))
        result['avg_clustering_coefficient'] += nonprofit['clustering_coefficient'] / float(len(nonprofits))
        if nonprofit['tw_community'] not in tw_communities:
            tw_communities[nonprofit['tw_community']] = 0
        else:
            tw_communities[nonprofit['tw_community']] += 1
        result['tw_communities'] = tw_communities
        if nonprofit['web_community'] not in web_communities:
            web_communities[nonprofit['web_community']] = 0
        else:
            web_communities[nonprofit['web_community']] += 1
        result['web_communities'] = web_communities
        if nonprofit['desc_community'] not in desc_communities:
            desc_communities[nonprofit['desc_community']] = 0
        else:
            desc_communities[nonprofit['desc_community']] += 1
        result['desc_communities'] = desc_communities

    return json.dumps(result)


@app.route('/possible_partners')
def related_companies():
    """Return the possible donors given a nonprofit"""
    attr = request.args.get('attr')
    if attr == 'description':
        query = "call  from_id_to_companies_by_desc('%d')" % int(request.args.get('id'))
    elif attr == 'homepage':
        query = "call  from_id_to_companies_by_home('%d')" % int(request.args.get('id'))
    elif attr == 'tweets':
        query = "call  from_id_to_companies_by_tweets('%d')" % int(request.args.get('id'))
    result = DBSession.execute(query)
    return json.dumps(procedure_to_json(result))


if __name__ == '__main__':
    app.run(debug=True)
