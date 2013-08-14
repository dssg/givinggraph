import logging

from gensim import corpora
from gensim.models.ldamodel import LdaModel


def get_topics(texts):
    topic_model = __get_topic_model(texts)
    topic_model.show_topics()


def __get_topic_model(texts):
    """Takes a list of strings as input. Returns a gensim.Similarity object for calculating cosine similarities."""
    texts_tokenized = [__tokenize_text(text) for text in texts]
    logging.debug('Creating corpora dictionary...')
    corpora_dict = corpora.Dictionary(texts_tokenized)
    logging.debug('Done creating corpora dictionary.')
    # gensim has us convert tokens to numeric IDs using corpora.Dictionary
    corpus = [corpora_dict.doc2bow(text_tokenized) for text_tokenized in texts_tokenized]
    return LdaModel(corpus, id2word=corpora_dict)


def __tokenize_text(text):
    """Convert text to lowercase, replace periods and commas, and split it into a list.
    >>> __tokenize_text('hi. I am, a, sentence.')
    ['hi', 'i', 'am', 'a', 'sentence']
    """
    return text.lower().replace(',', '').replace('.', '').split()
