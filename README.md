GivingGraph
========
Giving Graph is a proof-of-concept project that **assembles information** about nonprofits scattered throughout the web, uses this data to **build a social network** that links nonprofits, companies, and people, and publishes the resulting "giving graph" through an **API.** This API could eventually be used to power apps that help non-profits understand which who to partner with, who to get funding from, and how to get more supporters.

This project is part of the 2013 [Data Science for Social Good](http://dssg.io) fellowship, in partnership with the [Case Foundation](http://casefoundation.org). The Giving Graph concept [was introduced by the Case Foundation](http://casefoundation.org/blog/how-new-type-social-graph-could-change-philanthropy) in early 2013.


## The Problem
Every nonprofit has three critical activities to consider: fundraising, attracting volunteers/employees, and forming partnerships. Unfortunately, nonprofits aren't learning as much from each other as they could. The problem isn't a lack of information. The problem is that there's too much and it's messy -- scattered across the web, in charity databases, in news articles, in social media, in sources organized and unorganized.

GivingGraph is an integration tool to help nonprofits understand their relationship to people, causes, companies, and other nonprofits. Some questions we aim to help nonprofits answer include:

1. How do I relate to other charities operating in the same sector?
2. Which companies have partnerships with nonprofits in my sector?
3. Which is my impact on social media and what are the characteristics of my followers?

## The Solution
GivingGraph automates the retrieval of information about nonprofits and the analysis of that information.

For a given nonprofit, the following kinds of data are collected:
* based on an EIN, basic nonprofit information is retrieved via the GuideStar.org API (nonprofit name, location, description, etc).
* news articles mentioning a nonprofit are retrieved by searching Yahoo News.
* the official Twitter account of a nonprofit is retrieved by searching Yahoo.
* the nonprofit's Twitter followers are retrieved.
* the nonprofit's tweets are retrieved.

The following kinds of analyses are performed:
* Similarity between nonprofits, based on tweets.
* Similarity between nonprofits, based on descriptions.
* Community membership, based on tweet similarity.
* Community membership, based on description similarity.

## The Project

### Structured Information
GivingGraph enables you to aggregate data from structured sources such as GuideStar and CharityNavigator (with appropriate API permissions). This step will provide information such as nonprofit name, financials, and categorization code.

### Unstructured Information
GivingGraph collects information connecting nonprofits and companies from the following sources:

- **News stories**: GivingGraph uses web search APIs to gather news stories containing mentions of nonprofits, companies, and causes. Filtering is performed to reduce false matches.
- **Webpages**: The data from Guidestar and CharityNavigator often contain the web addresses of each nonprofit. The tool can crawl these pages and extract names of companies, using a combination of lists of company names.

This step provides information such as the causes and nonprofits a company supports.

Social information: For each nonprofit, GivingGraph attempts to identify their Twitter account(s) and analyze their follower list to derive information such as number of followers.

### Graph Analysis
With these sources of information, we can then build a weighted graph connecting nonprofits, causes, companies, and people. Community detection algorithms can then be used to detect related nonprofits recommend partnerships.


## Installation Guide

    git clone https://github.com/dssg/givinggraph.git
    cd givinggraph
    python setup.py install

### API Configuration
Various API and database credentials are read from a configuration file. A sample file is provided: [`sample.cfg`](https://github.com/dssg/givinggraph/blob/master/sample.cfg). You should:

1. copy sample.cfg to somewhere else (e.g., `~/.giving`)
2. add your credentials
3. set an environment GGRAPH_CFG to point to the file (e.g., `export GGRAPH_CFG=~/.giving`)

For the full experience, you'll need credentials for [GuideStar](http://www.guidestar.org/), [Charity Navigator](http://www.charitynavigator.org/), [Twitter](http://twitter.com). Also, you'll need to launch a MySQL instance and enter your host information in the config.

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
