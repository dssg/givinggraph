import logging

from gensim import corpora
from gensim.models.ldamodel import LdaModel
from nltk.corpus import stopwords


def get_topics(texts):
    topic_model = __get_topic_model(texts)
    topic_model.show_topics()


def __get_topic_model(texts):
    """Takes a list of strings as input. Returns an LDA model."""
    texts_tokenized = [__tokenize_text(text) for text in texts]

    logging.debug('Creating corpora dictionary...')
    corpora_dict = corpora.Dictionary(texts_tokenized)
    stop_word_ids = [corpora_dict.token2id[stop_word] for stop_word in __get_stop_words() if stop_word in corpora_dict.token2id]
    corpora_dict.filter_tokens(stop_word_ids)
    corpora_dict.filter_extremes(no_below=2, no_above=.99)
    corpora_dict.compactify()

    logging.debug('Done creating corpora dictionary.')
    # gensim has us convert tokens to numeric IDs using corpora.Dictionary
    corpus = [corpora_dict.doc2bow(text_tokenized) for text_tokenized in texts_tokenized]
    return LdaModel(corpus, id2word=corpora_dict, passes=3, num_topcs=50)


def __tokenize_text(text):
    """Convert text to lowercase, replace punctuation, remove words that are two character or less, and split the resulting string into a list.
    >>> __tokenize_text('hi. I am, a, sentence.')
    ['sentence']
    """

    text = text.lower()
    
    punctuation = ',.<>:;"\'~`@#^*()-_+=|\\/?!'
    for p in punctuation:
        text = text.replace(p, ' ')
    
    words = text.split()
    final_list = []
    for word in words:
        if len(word) > 2:
            final_list.append(word)

    return final_list


def __get_stop_words():
    stop_words = stopwords.words('english')
    stop_words.extend(['rt', 'its', "it's", 'great', 'thank', 'thanks', 'like', '&amp', 'pls', 'us', 'via', '&', 'get', 'please', 'http'])
    return stop_words
