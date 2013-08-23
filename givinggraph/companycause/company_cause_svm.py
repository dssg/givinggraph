#!/usr/bin/env python
#
# Description: This runs a support vector machine (SVM) on the
#	labelled dataset (company summary, donation cause).
#

import pickle
import string
import re
import numpy as np

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cross_validation, metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
#from sklearn.naive_bayes import MultinomialNB
#from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelBinarizer, LabelEncoder
from sklearn.svm import LinearSVC

MATCHED_DATA= 'company_aboutus_cause_match.p'
punct_re = re.compile('[%s]' % re.escape(string.punctuation))

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
	stop = stopwords.words('english')
	return [t for t in toks if t not in company_words and t not in stop and len(t)>3]

def main():
	# Load training data
	global company_words
	company2causes,causes,company2page,company_words = pickle.load(open(MATCHED_DATA,'rb'))

	del company2causes['COMPANY NAME']
	causes.discard('STANDARD CAUSE')


	companies = company2page.keys()
	#pipeline = CountVectorizer(tokenizer=tokenize)
	pipeline = TfidfVectorizer(tokenizer=tokenize)
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
		pred = clf.fit(X[list(train)], Y[list(train)])
		pred = pred.predict(X[test])
		losses.append(metrics.precision_score(truth.reshape(-1), pred.reshape(-1)))
	print 'F1 score=%.3f stderr=%.3f' % (np.average(losses), np.std(losses))

	# Retrain on all to print top words
	clf.fit(X, Y)
	print_top_words(pipeline, clf, label_enc.classes_, 20)

if __name__ == '__main__':
	main()

