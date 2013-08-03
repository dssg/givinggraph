import givinggraph.yahoo.search as yahoo
import givinggraph.news.parser as parser
import requests
from collections import namedtuple

Article = namedtuple('Article', 'url headline body')


def find_news_articles(nonprofit_name, urls_to_ignore=[]):
    """Searches Yahoo News for the given nonprofit name and returns a list of URLs, where each URL is a search result. Optionally takes a list of URLs to filter out of the results."""
    articles = []
    for url in yahoo.get_news_results(nonprofit_name):
        if url not in urls_to_ignore:
            html = requests.get(url).text
            headline, body = parser.get_article_parts(html)
            articles.append(Article(url, headline, body))
    return articles
