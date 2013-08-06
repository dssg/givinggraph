import doctest
import givinggraph.news.parser


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(givinggraph.news.parser))
    return tests
