'''
Set of RESTful endpoints to query the giving database.  See README.md for
documentation.
'''
# FIXME: Use SQLAlchemy instead of raw sql


import json

from flask import Flask
import MySQLdb
import MySQLdb.cursors

import givinggraph.config as config

app = Flask(__name__)
db = None


def select(stmt, args):
    'Return results of a select query.'
    cur = db.cursor()
    cur.execute(stmt, args)
    return cur.fetchall()


@app.route('/nonprofit/ein/<ein_id>')
def by_ein(ein_id):
    '''lookup nonprofit by EIN.'''
    return json.dumps(select('select * from nonprofits where ein=%s', (ein_id)))


@app.route('/nonprofit/id/<nonprofit_id>')
def by_id(nonprofit_id):
    '''lookup nonprofit by our internal id. Note that this violates DRY a bit
    (wrt to by_ein) to avoid SQL injection on column names.'''
    return json.dumps(select('select * from nonprofits where nonprofits_id=%s',
                             (nonprofit_id)))


def init_db():
    'Create connection to the mysql database specified in --config.'
    global db
    db = MySQLdb.connect(host=config.read_config('database', 'host'),
                         user=config.read_config('database', 'user'),
                         passwd=config.read_config('database', 'pass'),
                         db=config.read_config('database', 'database'),
                         cursorclass=MySQLdb.cursors.DictCursor)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
