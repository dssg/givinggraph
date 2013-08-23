#!/usr/bin/env python
#
# Description: This takes the company-cause relationship
# data and pickles it for the classifier to run on.
#

import argparse
from collections import defaultdict
import io
import re
import pickle
import string


company_words = set()
punct_re = re.compile('[%s]' % re.escape(string.punctuation))

def read_causes(filename):
        global company_words
        causes = set()
        co2causes = defaultdict(lambda: set())
        for line in io.open(filename, mode='rt'):
                parts = line.strip().split('\t')
                co2causes[parts[2]].add(parts[7])
                causes.add(parts[7])
                company_words |= set(do_tokenize(parts[2]))
        return co2causes, causes


def do_tokenize(s):
        s = punct_re.sub(' ', s.lower())
        s = re.sub('\s+', ' ', s)
        return s.strip().split()


def tokenize(s):
        global company_words
        toks = do_tokenize(s)
        return [t for t in toks if t not in company_words]


def read_pages(filename, co2causes):
        """Read company web page file, retaining only those in co2causes"""
        co2page = dict()
        for line in io.open(filename, mode='rt', encoding='latin_1'):
                parts = line.strip().split('\t')
                if parts[1] in co2causes and len(parts) > 2:
                        co2page[parts[1]] = ' '.join([parts[i] for i in range(3,len(parts),2)])
        return co2page


if __name__ == '__main__':
        global company_words

        ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
        ap.add_argument('--homepages',
                        metavar='HOMEPAGES',
                        default='company_aboutus.tsv',
                        help='file in format company_name<TAB>web_text')
        ap.add_argument('--causes',
                        metavar='CAUSES',
                        default='company_causes.tsv',
                        help='file in format company_name<TAB>cause . Note that companies may appear more than once.')
        args = ap.parse_args()

        company2causes, causes = read_causes(args.causes)
        print 'read %d companies with causes' % len(company2causes.keys())
        company2page = read_pages(args.homepages, company2causes)
        print 'read %d homepages' % len(company2causes.keys())
        
        # Pickle results
        pickle.dump((dict(company2causes),causes,company2page,company_words),open('company_cause_results.p','wb'))
