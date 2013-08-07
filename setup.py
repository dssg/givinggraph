from setuptools import setup, command
import os
import sys
import urllib
import tarfile

'''setuptools works by triggering subcommands from higher level commands.
The default commands 'install' and 'develop' trigger the following sequences:

install:
  1. build
  2. build_py
  3. install_lib
  4. install_egg_info
  5. egg_info
  6. install_scripts

develop:
  1. egg_info
  2. build_ext
'''

setup(
    name='givinggraph',
    version='0.0.1',
    packages=['givinggraph'],
    install_requires=[
        'BeautifulSoup',
        'celery',
        'gensim',
        'goose-extractor',  # see dependency link since not in pypi
        # 'matplotlib', # ignoring for now to see if travis stops complaining
        'networkx',
        'sqlalchemy',
    ],
    dependency_links=[
        'http://github.com/grangier/python-goose/tarball/master/#egg=goose-extractor-1.0.1'
    ],
    entry_points={
        'console_scripts': [
            'givinggraph-ui = givinggraph.ui:main',
        ],
    },
    tests_require=[
        'nose',
        'pep8',
        'pyflakes',
    ],
    test_suite='tests',
)
