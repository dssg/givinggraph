import subprocess
from BeautifulSoup import BeautifulSoup as bs
from urllib import urlencode


def get_top_search_result(search_terms):
    URL = 'http://search.yahoo.com/search?'
    fields = {'p': search_terms.strip()}

    response = subprocess.Popen(['phantomjs', 'curlweb2.0', URL + urlencode(fields)], stdout=subprocess.PIPE)
    soup = bs(response.stdout.read())

    results = soup.findAll(attrs={'class': 'res'})

    handle = ''
    if results:
        first_url = results[0].find(attrs={'class': 'url'})  # we're just going to take the first as best. flawed, but what can you do.
        if len(first_url.contents) > 2:
            for entry in first_url.contents[2:]:
                handle += entry.string

    return handle.encode('utf-8')
