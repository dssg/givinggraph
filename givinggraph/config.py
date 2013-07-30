from requests_oauthlib import OAuth1
import argparse
import ConfigParser
import os

ap = argparse.ArgumentParser(description=__doc__,
                             formatter_class=argparse.RawTextHelpFormatter)
ap.add_argument('--config',
                metavar='CONFIG',
                default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.cfg'),
                help='config file, containing keys and login info')
args = ap.parse_args()


def read_config(section_name, item_name):
    config = ConfigParser.RawConfigParser()
    config.read(os.environ['GGRAPH_CFG'])
    #config.read(args.config)
    return config.get(section_name, item_name)


def get_twitter_authentication():
    return OAuth1(read_config('twitter', 'client_key'),
                  client_secret=read_config('twitter', 'client_secret'),
                  resource_owner_key=read_config('twitter', 'resource_owner_key'),
                  resource_owner_secret=read_config('twitter', 'resource_owner_secret'))
