from requests_oauthlib import OAuth1
import ConfigParser
import os


def read_config(section_name, item_name):
    """Return the config value for the given section and item names."""
    config = ConfigParser.RawConfigParser()
    config.read(os.environ['GGRAPH_CFG'])
    return config.get(section_name, item_name)


def get_twitter_authentication():
    """Return the OAuth token for Twitter's API."""
    return OAuth1(read_config('twitter', 'client_key'),
                  client_secret=read_config('twitter', 'client_secret'),
                  resource_owner_key=read_config('twitter', 'resource_owner_key'),
                  resource_owner_secret=read_config('twitter', 'resource_owner_secret'))
