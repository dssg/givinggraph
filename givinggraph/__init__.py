import os
import logging
import logging.config

# just resolve this file in the context of the current working directory
# and find the parent of its directory
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# create logger
logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)
