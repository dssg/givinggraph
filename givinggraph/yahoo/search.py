import re
import requests
from BeautifulSoup import BeautifulSoup as bs
from urllib import urlencode


def get_search_results(search_terms):
    URL = 'http://search.yahoo.com/search?'
    fields = {'p': search_terms.strip()}
    soup = bs(requests.get(URL + urlencode(fields)).text)
    return [re.sub('<[^>]+>', '', str(hit.find(attrs={'class': 'url'}))) for hit in soup.findAll(attrs={'class': 'res'})]

def get_news_results(search_terms):
    URL = 'http://news.search.yahoo.com/search?'
    fields = {'p': search_terms.strip()}
    soup = bs(requests.get(URL + urlencode(fields)).text)
    return [hit['href'] for hit in soup.findAll(attrs={'class': 'yschttl spt'}) if hit['href'][:7] == 'http://']
