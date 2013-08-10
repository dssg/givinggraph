import logging

import numpy
from gensim import corpora, models
from gensim.similarities.docsim import Similarity


def get_similarity_scores_all_pairs(texts):
    """Takes a list of strings as input and returns a matrix of cosine similarity values where element [m][n] represents the similarity between text m and text n.
    >>> get_similarity_scores_all_pairs(['apple banana', 'banana cherry'])
    array([[ 1.,  0.],
           [ 0.,  1.]])
    """
    n = len(texts)
    all_similarities = numpy.empty(shape=(n, n))
    similarity_index = __get_tfidf_similarity_index(texts)

    for i in xrange(n):
        all_similarities[i] = similarity_index.similarity_by_id(i)
    return all_similarities


def __get_tfidf_similarity_index(texts):
    """Takes a list of strings as input. Returns a gensim.Similarity object for calculating cosine similarities."""
    texts_tokenized = [__tokenize_text(text) for text in texts]
    logging.debug('Creating corpora dictionary...')
    corpora_dict = corpora.Dictionary(texts_tokenized)
    logging.debug('Done creating corpora dictionary.')
    # gensim has us convert tokens to numeric IDs using corpora.Dictionary
    corpus = [corpora_dict.doc2bow(text_tokenized) for text_tokenized in texts_tokenized]
    corpus_tfidf = models.TfidfModel(corpus, normalize=True)[corpus]  # Feed corpus back into its own model to get the TF-IDF values for the texts

    logging.debug('Creating Similarity index...')
    index = Similarity(None, corpus_tfidf, num_features=len(corpora_dict))
    logging.debug('Done creating Similarity index.')
    return index


def __tokenize_text(text):
    """Convert text to lowercase, replace periods and commas, and split it into a list.
    >>> __tokenize_text('hi. I am, a, sentence.')
    ['hi', 'i', 'am', 'a', 'sentence']
    """
    return text.lower().replace(',', '').replace('.', '').split()
