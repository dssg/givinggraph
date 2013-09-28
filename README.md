GivingGraph
========
Giving Graph is a proof-of-concept project that **assembles information** about nonprofits scattered throughout the web, uses this data to **build a social network** that links nonprofits, companies, and people, and publishes the resulting "giving graph" through an **API.** This API could eventually be used to power apps that help non-profits understand which who to partner with, who to get funding from, and how to get more supporters.

This project is part of the 2013 [Data Science for Social Good](http://dssg.io) fellowship, in partnership with the [Case Foundation](http://casefoundation.org). The Giving Graph concept [was introduced by the Case Foundation](http://casefoundation.org/blog/how-new-type-social-graph-could-change-philanthropy) in early 2013.


## The Problem: knowledge gaps in the nonprofit sector
Every nonprofit has three critical activities to consider: fundraising, attracting volunteers/employees, and forming partnerships. Unfortunately, nonprofits aren't learning as much from each other about how to do these things as they could. The problem isn't a lack of information about what other organizations do. There's a ton out there, but it's messy -- scattered across the web, in charity databases, in news articles, in social media, in data sources structured and unstructured.

GivingGraph is a data aggregation tool to help nonprofits understand their relationship to people, companies, and other nonprofits. The key questions we aim to help nonprofits answer:

1. How do I relate to other charities operating in the same sector?
2. Which companies have partnerships with nonprofits in my sector?
3. What is my impact on social media, and what are the characteristics of my followers?

For more info, see the wiki page: http://github.com/dssg/givinggraph/wiki/Problem

## The Solution: data gathering, text mining, social network analysis, and APIs
GivingGraph 1. gathers disparate information about nonprofits from structured, unstructured, and social sources, 2. constructs a network of nonprofits/companies/people from this information, and 3. makes the resulting "giving graph" available to everyone through an **API**. 

Apps can then be built on top of this API to help nonprofits answer their burning questions about their nonprofit peers, potential corporate partners, and followers. 

### Structured data - basic info on nonprofits
GivingGraph enables you to aggregate basic information about a nonprofit from structured databases such as GuideStar and CharityNavigator, with appropriate API permissions and the organization's nonprofit ID (EIN number).

* Nonprofit's name, location, description, financials, and issue category (NTEE code).

### Unstructured data - nonprofits, and companies
GivingGraph fetches unstructured, natural language data from the web in order to link nonprofits to companies:

- **News articles**: GivingGraph uses web search APIs like Yahoo News to gather news stories that mention companies and the nonprofits and causes they support. Filtering is performed to reduce false matches.
- **Webpages**: the Guidestar and CharityNavigator databases often list a nonprofit's homepage. Givinggraph can crawl these webpages and automatically extract company names that pop up - possibly indicating a relationship - using a combination of lists of company names.

### Social data - nonprofits and supporters
GivingGraph can also fetch a nonprofit's twitter data:

- the organization's official **twitter account**, by searching Yahoo.
- the nonprofit's **twitter followers**, from the Twitter API.
- the nonprofit's **tweets**, from the same place.

### Graph building - linking everything together
With all these sources of information in hand, we use **natural language processing** techniques to build a **weighted graph** that connects nonprofits, companies, and people (twitter followers). 

- Similarity relationships between nonprofits, based on their tweets.
- Similarity relationships between nonprofits, based on their webpages.
- Follower relationships between twitter users and nonprofits.
- Relationships between companies and nonprofits, based on news article mentions.

### Graph analysis - understanding supports, recommending partnerships, finding nonprofit communities, understanding connectedness
We then use **social network analysis**, including **community detection algorithms**, to recommend company partnerships, discover communities of similar nonprofits, and understand the network structure of those communities.

- Basic twitter account summary stats, including average retweets and favorites. (this part of the analysis is very undeveloped).
- Companies the nonprofit could partner with, based on firms mentioned in news articles with similar organizations
- Social network analysis of individual nonprofits: how connected they are to other organizations, etc.
- Social network analysis of nonprofit verticals: how well connected environmental organizations are, etc.

# Giving graph API - publishing the graph and analysis
In order for the nonprofit-company graph we've constructed and the analysis we're doing on top of it to be useful, we make them available through a simple [API](https://github.com/dssg/givinggraph/wiki/API). Apps can be built on top of this API that help nonprofits answer key questions, thus alleviating knowledge gaps in the sector.

## Project Layout
* [`/givinggraph`](givinggraph) contains a Python package for retrieving and analyzing nonprofit data. It's the heart of the project.
* [`/db`](db) contains SQL scripts that create a database to put nonprofit data in, and various scripts for retrieving data from the DB.
* [`/scripts`](scripts) contains R code for visualizing this nonprofit data.

* [`/docs`](docs) contains presentation slides about the project.
* [`/tests`](tests) contains Python for checking for pep8 violations.

## Installation Guide
GivingGraph has been tested with Python 2.7 and MySQL 5.5.31.

    git clone https://github.com/dssg/givinggraph.git
    cd givinggraph
    python setup.py install

### API Configuration
Various API and database credentials are read from a configuration file. A sample file is provided: [`sample.cfg`](https://github.com/dssg/givinggraph/blob/master/sample.cfg). You should:

1. copy sample.cfg to somewhere else (e.g., `~/.giving`)
2. add your credentials
3. set an environment GGRAPH_CFG to point to the file (e.g., `export GGRAPH_CFG=~/.giving`)

For the full experience, you'll need credentials for [GuideStar](http://www.guidestar.org/), [Charity Navigator](http://www.charitynavigator.org/), [Twitter](http://twitter.com). Also, you'll need to launch a MySQL instance and enter your host information in the config.

For more info, see the wiki: https://github.com/dssg/givinggraph/wiki/API

### Celery Configuration

NOTE: Due to a race condition, Celery is not currently being used. See [issue #19](https://github.com/dssg/givinggraph/issues/19).

GivingGraph uses Celery to schedule asynchronous tasks (like web crawling, API
calls, etc). This depends on [RabbitMQ](http://www.rabbitmq.com/) to track
tasks. RabbitMQ is available in most package installers (e.g., `brew install
rabbitmq`).

Below is an example of launching a celery worker, then running a script to test it out:

```
celery -A givinggraph.tasks worker --loglevel=INFO
python -m givinggraph.tasks
```

## Contributing to the Project
- Feel free to create an issue for any bugs you encounter.
- To get involved with this project, reach out to <dssg-giving@googlegroups.com>

[Travis](https://travis-ci.org/dssg/givinggraph) is used for continuous testing. Most of the tests are [doctests](http://docs.python.org/2/library/doctest.html).

## License
MIT license, see [LICENSE.txt](LICENSE.txt)
