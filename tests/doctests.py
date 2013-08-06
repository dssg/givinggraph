import doctest
import givinggraph.news.parser
import givinggraph.util.text2tfidf


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(givinggraph.news.parser))
    tests.addTests(doctest.DocTestSuite(givinggraph.util.text2tfidf))
    return tests
