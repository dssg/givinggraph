''' Convert text into tf-idf.
usage: python data_loader.py TEXT_FILE

File should have one document per row. E.g. this file:

apple banana
banana cherry

results in

1:0.579739 0:0.814802
2:0.814802 1:0.579739

with a vocabulary of

[(u'apple', 0), (u'banana', 1), (u'cherry', 2)]

'''

import io
import operator
import sys


from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


def text2tfidf(data_generator):
    '''Transform text data into tf-idf vectors. This can be used in a
    streaming fashion, so that each line is represented sparsely as its read.

    data_generator .... generator of strings. This can simply be a list of
    strings, or a file object.

    >>> vocab, data = text2tfidf(['apple banana', 'banana cherry'])
    >>> data = data.toarray()
    >>> print data[0]
    [ 0.81480247  0.57973867  0.        ]
    >>> print data[1]
    [ 0.          0.57973867  0.81480247]
    >>> print sorted(vocab.iteritems(), key=operator.itemgetter(1))
    [(u'apple', 0), (u'banana', 1), (u'cherry', 2)]
    '''
    counter = CountVectorizer(min_df=0.)
    data = counter.fit_transform(data_generator)
    tfidf = TfidfTransformer()
    data = tfidf.fit_transform(data)
    return counter.vocabulary_, data


def print_sparse_matrix(data):
    'Print a sparse matrix in format <index>:<value>'
    for ri in range(data.get_shape()[0]):
        row = data.getrow(ri)
        print ' '.join(['%d:%g' % (i, d)
                        for (i, d) in zip(row.indices, row.data)])


if (__name__ == '__main__'):
    if len(sys.argv) == 1:
        print 'python data_loader.py TEXT_FILE'
    vocab, data = text2tfidf(io.open(sys.argv[1], mode='rt', encoding='utf8'))
    print_sparse_matrix(data)
