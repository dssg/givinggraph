""" Predict whether a company supports a cause based on its web presence.  We
train a model based on the data at milliondollarlist.org, which posts
donations of $1M or more from companies to causes."""

# FIXME: read/write from database.
# FIXME: save/load classifier

import argparse
from collections import defaultdict
import io
import re
import string

import numpy as np
from sklearn import cross_validation, metrics
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
#from sklearn.naive_bayes import MultinomialNB
#from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelBinarizer, LabelEncoder
from sklearn.svm import LinearSVC


company_words = set()
punct_re = re.compile('[%s]' % re.escape(string.punctuation))


def read_causes(filename):
    global company_words
    causes = set()
    co2causes = defaultdict(lambda: set())
    for line in io.open(filename, mode='rt'):
        parts = line.strip().split('\t')
        co2causes[parts[0]].add(parts[1])
        causes.add(parts[1])
        company_words |= set(do_tokenize(parts[0]))
    return co2causes, causes


def read_pages(filename, co2causes):
    """Read company web page file, retaining only those in co2causes"""
    co2page = dict()
    for line in io.open(filename, mode='rt', encoding='latin_1'):
        parts = line.strip().split('\t')
        if parts[0] in co2causes and len(parts) > 1:
            co2page[parts[0]] = parts[1]
    return co2page


def print_top_words(vectorizer, clf, class_labels, n=10):
    """Prints features with the highest coefficient values, per class"""
    feature_names = vectorizer.get_feature_names()
    for i, class_label in enumerate(class_labels):
        topn = np.argsort(clf.coef_[i])[-n:]
        print("%s: %s" % (class_label,
              " ".join(feature_names[j] for j in topn)))


def do_tokenize(s):
    s = punct_re.sub(' ', s.lower())
    s = re.sub('\s+', ' ', s)
    return s.strip().split()


def tokenize(s):
    global company_words
    toks = do_tokenize(s)
    return [t for t in toks if t not in company_words]


if (__name__ == '__main__'):
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

    company2causes, causes = read_causes(args.causes)
    print 'read %d companies with causes' % len(company2causes.keys())
    company2page = read_pages(args.homepages, company2causes)
    print 'read %d homepages' % len(company2causes.keys())
    companies = company2page.keys()
    pipeline = CountVectorizer(tokenizer=tokenize)
    X = pipeline.fit_transform([company2page[c] for c in companies])
    # convert labels to multilabel format
    Y = np.array([list(company2causes[c]) for c in companies])
    N = len(Y)
    label_enc = LabelEncoder()
    label_enc.fit(list(causes))
    print 'found %d causes' % len(label_enc.classes_)
    Y = [list(label_enc.transform(yi)) for yi in Y]
    print 'labels:', label_enc.classes_
    # LabelBinarizer buggy with np arrays. See https://github.com/scikit-learn/scikit-learn/issues/856
    Y = LabelBinarizer().fit_transform(Y)
    #clf = OneVsRestClassifier(MultinomialNB())
    #clf = OneVsRestClassifier(LogisticRegression())
    clf = OneVsRestClassifier(LinearSVC(random_state=0))

    cv = cross_validation.KFold(len(Y), 10, shuffle=True, random_state=1234)
    losses = []
    for train, test in cv:
        truth = Y[test]
        pred = clf.fit(X[train], Y[train]).predict(X[test])
        losses.append(metrics.precision_score(truth.reshape(-1), pred.reshape(-1)))
    print 'F1 score=%.3f stderr=%.3f' % (np.average(losses), np.std(losses))

    # Retrain on all to print top words
    clf.fit(X, Y)
    print_top_words(pipeline, clf, label_enc.classes_, 20)
