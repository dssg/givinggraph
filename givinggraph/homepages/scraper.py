import requests


def get_webpage_html(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    else:
        return r.text
