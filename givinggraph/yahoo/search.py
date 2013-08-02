import requests
from BeautifulSoup import BeautifulSoup as bs
from urllib import urlencode


def get_search_results(search_terms):
    """Get a list of URLs by searching Yahoo with the given search terms."""
    return __search__('http://search.yahoo.com/search?', search_terms)


def get_news_results(search_terms):
    """Get a list of URLs by searching Yahoo News with the given search terms."""
    return __search__('http://news.search.yahoo.com/search?', search_terms)


def __search__(base_url, search_terms):
    """Given the URL of a Yahoo search result page, return the URLs of each website in the search results (a list of strings)."""
    fields = {'p': search_terms.strip(), 'n': 30}  # n is for the number of search results to display on one page
    soup = bs(requests.get(base_url + urlencode(fields)).text)
    return [hit['href'] for hit in soup.findAll(attrs={'class': 'yschttl spt'}) if hit['href'][:7] == 'http://']
