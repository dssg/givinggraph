## Overview
Here we provide a RESTful interface to our nonprofit analysis using [Flask](http://flask.pocoo.prg).

app.py queries a MySQL database and returns JSON objects.

See [API](https://github.com/dssg/givinggraph/wiki/API) for full documentation.

To run in production, we use gunicorn, listening on 7000:
`gunicorn  givinggraph.api.app:app --bind 0.0.0.0:7000`


