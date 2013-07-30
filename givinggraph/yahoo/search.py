import os
import subprocess
from BeautifulSoup import BeautifulSoup as bs
from urllib import urlencode


def get_top_search_result(search_terms):
    URL = 'http://search.yahoo.com/search?'
    fields = {'p': search_terms.strip()}

    phantomjs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'phantomjs')
    curlweb2_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'curlweb2.0')
    response = subprocess.Popen([phantomjs_path, curlweb2_path, URL + urlencode(fields)], stdout=subprocess.PIPE)
    soup = bs(response.stdout.read())

    results = soup.findAll(attrs={'class': 'res'})

    first_url = ''
    if results:
        first_url_parts = results[0].find(attrs={'class': 'url'})  # we're just going to take the first as best. flawed, but what can you do.
        for entry in first_url_parts.contents:
            first_url += entry.string

    return first_url.encode('utf-8')