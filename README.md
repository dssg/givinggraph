GivingGraph
========
[<img src="http://dssg.io/img/partners/case.jpg" width="400" align="right">](http://casefoundation.org)

Giving Graph is a proof-of-concept project that **assembles information** about nonprofits scattered throughout the web, uses this data to **build a social network** that links nonprofits, companies, and people, and publishes the resulting "giving graph" through an **API.** This API could eventually be used to power apps that help non-profits understand which who to partner with, who to get funding from, and how to get more supporters.

This project is part of the 2013 [Data Science for Social Good](http://dssg.io) fellowship, in partnership with the [Case Foundation](http://casefoundation.org). The Giving Graph concept [was introduced by the Case Foundation](http://casefoundation.org/blog/how-new-type-social-graph-could-change-philanthropy) in early 2013.


## The Problem: knowledge gaps in the nonprofit sector
Every nonprofit has three critical activities to consider: fundraising, attracting volunteers/employees, and forming partnerships. Unfortunately, nonprofits aren't learning as much from each other about how to do these things as they could. 

The problem isn't a lack of information about what other organizations do. There's a ton out there, but it's messy -- scattered across the web, in charity databases, in news articles, in social media, in data sources structured and unstructured.

If we brought all this info together, we could help nonprofits answer these key questions:

- How do I relate to other charities operating in the same sector?
- Which companies have partnerships with nonprofits in my sector?
- What is my impact on social media, and what are the characteristics of my followers?

**[Read more about the knowledge gap problem in the wiki](http://github.com/dssg/givinggraph/wiki/Problem)*

## The Solution: data gathering, topic modeling (NLP), community detection (network analysis), and APIs

![web app screenshot](https://raw.github.com/dssg/dssg.github.io/master/img/posts/givinggraph-screenshot.png)

To help nonprofits answer these questions, we've built GivingGraph, a data aggregation and analysis tool that helps these organizations understand their relationship to people, companies, and other nonprofits.

First, the tool gathers and merges disparate information about nonprofits from structured, unstructured, and social sources. Then, it constructs a network of nonprofits/companies/people from this information using text mining, and analyzes this graph using social network analysis. Finally, it makes this "giving graph" and analysis available to everyone through an **API**. 

Apps can then be built on top of this API to help nonprofits answer their burning questions about their nonprofit peers, potential corporate partners, and followers. 

**[Read up on how we're doing this in the wiki](http://github.com/dssg/givinggraph/wiki/Methodology)**

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


## Team
![Team](https://raw.github.com/dssg/dssg.github.io/761993c24ea2991170ef64048115cb805f5f13fb/img/people/teams/givinggraph.png)

## Contributing to the Project
- Feel free to create an issue for any bugs you encounter.
- To get involved with this project, reach out to <dssg-giving@googlegroups.com>

[Travis](https://travis-ci.org/dssg/givinggraph) is used for continuous testing. Most of the tests are [doctests](http://docs.python.org/2/library/doctest.html).

## License
MIT license, see [LICENSE.txt](LICENSE.txt)
