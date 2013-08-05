GivingGraph
========
A tool to help understand the relationships between non-profits, for-profits, and the causes they support.

GivingGraph is a project of the 2013 [Data Science for Social Good](http://dssg.io) fellowship, in partnership with the [Case Foundation](http://casefoundation.org). The Giving Graph concept [was introduced by the Case Foundation](http://casefoundation.org/blog/how-new-type-social-graph-could-change-philanthropy) in early 2013.


## Motivation

Three critical activities for nonprofits are fundraising, attracting volunteers, and forming partnerships. Strategies for achieving these aims vary widely across sectors, but there is little collaboration among nonprofits. In short, nonprofits aren't learning as much from each other as they could. There's too much information out there on non-profits scattered across the web, in charity databases, in news articles, in social media, in sources organized and unorganized.

This hinders decision making, since nonprofits have no complete picture of themselves within their sector. They can learn how to be more effective from their peers, if only they knew who their peers were and what their peers do. Reducing the burden of these tasks will allow nonprofits to focus on their core missions. 

In addition, the lack of a complete picture makes it difficult for individuals who want to help or donate. What if you want to figure out whom to donate to? How do you know to support, say, The American Cancer Society versus the Susan G. Komen Foundation?

GivingGraph is an integration tool to help nonprofits understand their relationship to people, causes, companies, and other nonprofits. Some questions we aim to help nonprofits answer include:

1. How do I relate to other charities operating in the same sector?
2. Which companies have partnerships with nonprofits in my sector?
3. Which is my impact on social media and what are the characteristics of my followers?

## Solution Overview and Use Cases

Our mission, then, is to provide nonprofits and individuals with sector-wide context so that they can make better and more informed decisions. 

The answers to their questions are already out there. They're just inaccessible, hard to find, scattered in different corners of the Internet. Below we list three critical tasks for non-profits and how we plan to support them:

### Partnerships (merge pre-existing databases and structured information)
If you want to know more about how your peers behave, there exist easily accessible tools like Guidestar and Charity Navigator, which inherit governmental work in classifying and documenting the non-profit sector. There's a hole in the existing information aggregate about regulatory actions taken against non-profits. If you want to know about how one of your peers' fundraisers failed to file their financial reports, and properly contextualize that with information about your peers' own financial information, then that can help you make more informed partnership decisions. The issue is that all this data doesn't exist in the same place, and employees then need to run from place to place grabbing information. We can provide one tool non-profits need to use. 

### Fundraising (unstructured data)
Say you're a smaller Chicago-based non-profit who focuses on educational programs. A New York-based organization who has provided funding for educational nonprofits has decided to expand and open an office in Chicago. They send out a press release, but if you're a smaller-sized non-profit, your ability to keep updated on news and press releases of your peer organizations is limited by your staff numbers. Maybe an intern is reading and flagging salient news articles. Very likely, this can slip right by you, and you rely on word on mouth to let you know about this new possible source of funding. However, we can automatically parse news text and press releases so that you can be updated on relevant events and not waste interns' or staff members' time painstakingly reading the news on all your peers, possible donors, and domain.

We don't have much structured information available on how non-profits interact with other companies, corporations included. That's available, though encased in natural language rather than databases. We'll pull those relationships using textual analysis on the web documents, like press releases and news stories. This component relies on natural language processing technology to extract information from web documents. 

### Individual engagement (social media)
Say a non-profit like WWF wants to find new partners, then we can look at their Twitter followers. Do they notice that their followers are criticizing fracking policies? Maybe they should start to co-sponsor events with anti-fracking activist organizations that their followers also follow. Or adopt a stance on anti-fracking. The tool can open up possibilities and facilitate decision-making, but won't dictate choices made by non-profits.

## Technical Approach
 
### Structured Information: 
GivingGraph enables you to aggregate data from structured sources such as GuideStar and CharityNavigator (with appropriate API permissions). 
 
This step will provide information such as nonprofit name, financials, and categorization code. 

### Unstructured Information:
GivingGraph collects information connecting nonprofits and companies from the following sources:

- **News stories**: GivingGraph uses web search APIs to gather news stories containing mentions of nonprofits, companies, and causes. Filtering is performed to reduce false matches.
- **Webpages**: The data from Guidestar and CharityNavigator often contain the web addresses of each nonprofit. The tool can crawl these pages and extract names of companies, using a combination of lists of company names.

This step provides information such as the causes and nonprofits a company supports.

Social information: For each nonprofit, GivingGraph attempts to identify their Twitter account(s) and analyze their follower list to derive information such as:

- no. followers, retweeters, favorites
- most frequent hashtags

### Graph Analysis
With these sources of information, we can then build a weighted graph connecting nonprofits, causes, companies, and people. Community detection algorithms can then be used to detect related nonprofits recommend partnerships.

## Contributing

To get started:

    git clone https://github.com/dssg/givinggraph.git
    cd givinggraph
    python setup.py develop

## Workflow
1. Make some changes
2. `git add <files>`; `git commit`
3. `git pull --rebase`
4. merge conflicts if needed
5. Make sure tests pass: `python setup.py test`
6. `git push`

[Travis](https://travis-ci.org/dssg/givinggraph) is used for continuous testing


## Configuration
Various API and database credentials are read from a configuration file. A sample file is provided: [`sample.cfg`](https://github.com/dssg/givinggraph/blob/master/sample.cfg). You should:

1. copy sample.cfg to somewhere else (e.g., `~/.giving`)
2. add your credentials
3. set an environment GGRAPH_CFG to point to the file (e.g., `export GGRAPH_CFG=~/.giving`)


### Celery
givinggraph uses Celery to schedule asynchronous tasks (like web crawling, API calls, etc). Below, we first launch a celery worker, then run a script to test it out:

```
celery -A givinggraph.tasks worker --loglevel=INFO
python -m givinggraph.tasks
```

## License
MIT License (MIT)

Copyright (c) 2013 John Brock, Giorgio Cavaggion, Kyla Cheung, Ahmad Qamar, Aron Culotta 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
