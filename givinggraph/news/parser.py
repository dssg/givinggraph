from goose import Goose
import re

EXCERPT_LOOK_AROUND_SIZE = 20  # how many characters to get before and after company name
FIND_COMPANY_SUFFIX_REGEX = re.compile(' (Inc|Corp|Co|Ltd)')

excerpt_regex_cache = {}
company_name_regex_cache = {}


def get_article_parts(html):
    '''Return headline, body'''
    g = Goose({'use_meta_language': False, 'enable_image_fetching': False})
    try:
        article = g.extract(raw_html=html)
    except:
        return None, None
    return article.title.strip().encode('utf-8'), article.title.strip().encode('utf-8')


def get_company_mentions_in_text(text, company_name):
    if company_name not in excerpt_regex_cache:
        __populate_regex_caches__(company_name)

    excerpts = []
    # the below if statement is an optimization: 'in' is fast, and checking for the company name by itself is faster than matching on the whole excerpt.
    if company_name.split()[0] in text and company_name_regex_cache[company_name].search(text) is not None:
        excerpts = excerpt_regex_cache[company_name].findall(text)  # match on the whole excerpt
    return excerpts


def __populate_regex_caches__(company_name):
    company_name_regex_text = __get_regexed_company_name_text__(company_name)
    company_name_regex_cache[company_name] = re.compile(company_name_regex_text)
    excerpt_regex_cache[company_name] = re.compile('(?:\w+\W{{1,5}}){{0,{before}}}{company}(?:\W{{1,5}}\w+){{0,{after}}}'.format(before=EXCERPT_LOOK_AROUND_SIZE, company=company_name_regex_text, after=EXCERPT_LOOK_AROUND_SIZE))


def __get_regexed_company_name_text__(company_name):
    return '\\b' + FIND_COMPANY_SUFFIX_REGEX.sub(',? \\1\\.?', re.escape(company_name)).strip() + '\\b'
