from goose import Goose
import re

EXCERPT_LOOK_AROUND_SIZE = 20  # how many words to get before and after company name
FIND_COMPANY_SUFFIX_REGEX = re.compile(' (Inc|Corp|Co|Ltd)')

excerpt_regex_cache = {}
company_name_regex_cache = {}


def get_article_parts(html):
    """Take HTML and return extracted headline and body."""
    g = Goose({'use_meta_language': False, 'enable_image_fetching': False})
    try:
        article = g.extract(raw_html=html)
    except:
        return None, None
    return article.title.strip().encode('utf-8'), article.cleaned_text.strip().encode('utf-8')


def get_company_mentions_in_text(text, company_name):
    """Finds mentions of a company in some text. Assumes company_name contains
        no puncutation (so "Apple Inc" instead of "Apple, Inc."), but the
        company name in text can contain punctuation.

        Test that context window size is correct:
        >>> context = 'x ' * EXCERPT_LOOK_AROUND_SIZE
        >>> match = get_company_mentions_in_text('should not return ' + context + ' Apple ' + context + ' should not return', 'Apple')[0]
        >>> 'Apple' in match
        True
        >>> 'should not return' in match
        False
    """
    if company_name not in excerpt_regex_cache:
        __populate_regex_caches__(company_name)

    excerpts = []
    # the below if statement is an optimization: 'in' is fast, and checking for the company name by itself is faster than matching on the whole excerpt.
    if text is not None and company_name.split()[0] in text and company_name_regex_cache[company_name].search(text) is not None:
        excerpts = excerpt_regex_cache[company_name].findall(text)  # match on the whole excerpt
    return excerpts


def __populate_regex_caches__(company_name):
    """Adds regexes for the given company name to company_name_regex_cache and excerpt_regex_cache."""
    company_name_regex_text = __get_regexed_company_name_text__(company_name)
    company_name_regex_cache[company_name] = re.compile(company_name_regex_text)
    excerpt_regex_cache[company_name] = re.compile('(?:\w+\W{{1,5}}){{0,{before}}}{company}(?:\W{{1,5}}\w+){{0,{after}}}'.format(before=EXCERPT_LOOK_AROUND_SIZE, company=company_name_regex_text, after=EXCERPT_LOOK_AROUND_SIZE))


def __get_regexed_company_name_text__(company_name):
    """Takes a company name and returns a regex string to account for possible punctuation in the company name."""
    return '\\b' + FIND_COMPANY_SUFFIX_REGEX.sub(',? \\1\\.?', re.escape(company_name)).strip() + '\\b'


def contains_supportive_wording(text):
    """Words found in news articles that relate companies to nonprofits in a positive way:
            partner
            partnership
            sponsor
            joins
            participating
            gave
            giving
            gift
            collaborated
            donation
            donate
            donor
            contribution
            contributor
            made possible by
            provided by
            provides
            providing
            teaming
            joined
            support
            help
            grant
            award

    >>> contains_supportive_wording('A partner is cool')
    True
    """

    supportive_words = ['partner',
                        'sponsor',
                        'participat',
                        'gave',
                        'giving',
                        'give',
                        'gift',
                        'collaborat',
                        'donat',
                        'donor',
                        'contribut',
                        'made possible by',
                        'provid',
                        'team',
                        'joins',
                        'joined',
                        'joining',
                        'support',
                        'help',
                        'grant',
                        'award']
    for word in supportive_words:
        if word in text:
            return True
    return False


def contains_opposing_wording(text):
    """Words found in news articles that relates companies to nonprofits in a negative way:
            criticism
            criticized
    """
    opposing_words = ['critic']
    for word in opposing_words:
        if word in text:
            return True
    return False
