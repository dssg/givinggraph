""" Predict whether a company supports a cause based on its web presence.  We
train a model based on the data at milliondollarlist.org, which posts
donations of $1M or more from companies to causes."""

import argparse
from collections import defaultdict
import io

import numpy as np
from sklearn import cross_validation, metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelBinarizer, LabelEncoder


ap = argparse.ArgumentParser(description=__doc__,
                             formatter_class=argparse.RawTextHelpFormatter)
ap.add_argument('--homepages',
                metavar='HOMEPAGES',
                default='company_pages.tsv',
                help='file in format company_name<TAB>web_text')
ap.add_argument('--causes',
                metavar='CAUSES',
                default='company_causes.tsv',
                help='file in format company_name<TAB>cause . Note that companies may appear more than once.')

args = ap.parse_args()


def read_causes(filename):
    co2causes = defaultdict(lambda: set())
    for line in io.open(filename, mode='rt'):
        parts = line.strip().split('\t')
        co2causes[parts[0]].add(parts[1])
    return co2causes


def read_pages(filename, co2causes):
    co2page = dict()
    for line in io.open(filename, mode='rt', encoding='latin_1'):
        parts = line.strip().split('\t')
        if parts[0] in co2causes and len(parts) > 1:
            co2page[parts[0]] = parts[1]
    return co2page


if (__name__ == '__main__'):
    company2causes = read_causes(args.causes)
    print 'read %d companies with causes' % len(company2causes.keys())
    company2page = read_pages(args.homepages, company2causes)
    print 'read %d homepages' % len(company2causes.keys())
    companies = company2page.keys()
    pipeline = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer())])
    X = pipeline.fit_transform([company2page[c] for c in companies])
    print X[0]

    # convert labels to multilabel format
    Y = np.array([list(company2causes[c]) for c in companies])
    N = len(Y)
    print Y[0]
    label_enc = LabelEncoder()
    # FIXME: why are there 83 labels? should be 21
    Y = label_enc.fit_transform(Y.reshape(-1)).reshape((N, -1))
    print Y[0]
    Y = LabelBinarizer().fit_transform(Y)
    print Y[0]
    clf = OneVsRestClassifier(LogisticRegression())

    #print cross_validation.cross_val_score(clf, X, Y, cv=10, scoring=metrics.hamming_loss)
    cv = cross_validation.KFold(len(Y), 10, shuffle=True, random_state=1234)
    losses = []
    for train, test in cv:
        truth = Y[test]
        pred = clf.fit(X[train], Y[train]).predict(X[test])
        losses.append(metrics.hamming_loss(truth, pred))
    print 'avg hamming los=%.2f stderr=%.2f' % (np.average(losses), np.std(losses))
