import numpy
from gensim import corpora, models, similarities


def get_simlarity_scores_for_all_pairs(texts):
    '''Takes a list of texts as input and returns a matrix, where element (m,n) represents the cosine similarity of texts[m] and texts[n].'''
    n = len(texts)
    similarity_result_matrix = numpy.empty(shape=(n, n))
    similarity_matrix = __get_corpus_tfidf_similarity_matrix__(texts)
    # for every row in the matrix, find its similarity to every other row
    for i, vec in similarity_matrix:
        similarity_result_matrix[i] = list(similarity_matrix[vec]) #  the [vec] notation returns a vector where each element is the cosine similarity value
    return similarity_result_matrix


def __get_corpus_tfidf_similarity_matrix__(texts):
    '''Takes a list of strings as input. Returns a gensim.similarities.SparseMatrixSimilarity object for calculating cosine similarities.'''
    # gensim has us convert tokens to IDs using corpora.Dictionary
    dictionary = corpora.Dictionary([text.lower().split() for text in texts])
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpus_tfidf = models.TfidfModel(corpus, normalize=True)[texts] #  Feed texts back into its own model to get the TF-IDF values for the texts
    return similarities.SparseMatrixSimilarity(corpus_tfidf)

# def add_tfidf_to(texts):
#     freq_dists = get_frequency_distributions(texts)
#     freq_dist_all = reduce(lambda x, y: x + y, freq_dists)

#     tf_idfs = []
#     for i, text in enumerate(texts):
#         idf = log(len(texts) / float())


#     tokens = {}
#     for id, doc in enumerate(documents):
#         get_frequency_distributions()

#         tf = {}
#         doc["tfidf"] = {}
#         doc_tokens = doc.get("tokens", [])
#         for token in doc_tokens:
#             tf[token] = tf.get(token, 0) + 1
#         num_tokens = len(doc_tokens)
#         if num_tokens > 0:
#             for token, freq in tf.iteritems():
#                 tokens.setdefault(token, []).append((id, float(freq) / num_tokens))

#     doc_count = float(len(documents))
#     for token, docs in tokens.iteritems():
#         idf = log(doc_count / len(docs))
#         for id, tf in docs:
#             tfidf = tf * idf
#             if tfidf > 0:
#                 documents[id]["tfidf"][token] = tfidf

#     for doc in documents:
#         doc["tfidf"] = normalize(doc["tfidf"])
#         print "**"

#     writer = csv.writer(open('similarities.csv','wb'),delimiter=';')
#     for i, document in enumerate(documents):
#         for document2 in documents[i+1:]:
#             print document['id'], document2['id'], cosine_distance(document, document2)
#             writer.writerow([document['id'], document2['id'], cosine_distance(document, document2)])


# def get_frequency_distributions(texts):
#     term_frequencies = [FreqDist(text.lower().split()) for text in texts]


# def normalize(features):
#     norm = 1.0 / sqrt(sum(i**2 for i in features.itervalues()))
#     for k, v in features.iteritems():
#         features[k] = v * norm
#     return features


# def cosine_distance(a, b):
#     cos = 0.0
#     a_tfidf = a["tfidf"]
#     for token, tfidf in b["tfidf"].iteritems():
#         if token in a_tfidf:
#             cos += tfidf * a_tfidf[token]
#     return cos
