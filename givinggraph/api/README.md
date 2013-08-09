## Overview
Here we provide a RESTful interface to our nonprofit analysis.

app.py queries a MySQL database and returns JSON objects.

FIXME: Add API documentation here

## API

- GET /nonprofit/ein/`ein` will return information on the nonprofit with the given EIN
- GET /nonprofit/id/`id` will return information on the nonprofit with the given ID

```json
[
  {
    "city": "Waitsfield",
    "twitter_name": "1PercentFTP",
    "description": "Using market forces to drive positive environmental change by inspiring companies to give.\r\nYvon Chouinard, founder of Patagonia, and Craig Mathews, owner of Blue Ribbon Flies, created the charity to encourage businesses to donate 1% of sales to environmental groups.",
    "ZIP": "5673\r",
    "mission_statement": "1% for the Planet exists to build and support an alliance of businesses financially committed to creating a healthy planet.",
    "twitter_id": "",
    "state": "VT",
    "ntee_code": "C12 (Fund Raising and/or Fund Distribution)",
    "nonprofit_id": 11117,
    "ein": "912151932",
    "name": "1% For The Planet"
  }
]
```

### Dependencies
- Flask: http://flask.pocoo.org

