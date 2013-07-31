''' Uses celery to ingest a new charity. This is a mix of serial and parallel
tasks, so we use celery to do this efficiently.

This depends on a running instance of a rabbitmq messaging server to keep
track of task statuses. This can be launched on our ec2 instance with:
~/rabbitmq/rabbitmq_server-3.1.3/sbin/rabbitmq-server . If you're developing
locally, you'll have to install rabbitmq (e.g., brew install rabbitmq).

For this script to work, you first need to run a celery worker process to
await orders. From the base dir:
$ celery -A givinggraph.tasks worker --loglevel=info

Then, you can call any of the functions below (see main for an example). To
test on a single nonprofit, run

$ python -m givinggraph.tasks

The worker task will print all the log messages. This is useful for seeing the
order in which tasks are actually executed.

FIXME: currently queries guidestar and logs result. Database is not modified.
FIXME: Add calls to all the other parts of the pipeline (news, twitter, etc)
FIXME: The REST api will be the one calling this in the future.
'''

from celery import Celery
from celery import chain, group

from .guidestar import search as gs
from .models import DBSession


'This is the extent of the celery configuration!'
celery = Celery('tasks',
                backend='amqp',
                broker='amqp://guest@localhost//')


@celery.task(name='tasks.guidestar')
def guidestar(ein):
    print 'guidestar', ein
    result = gs.get_nonprofit(ein)
    print result
    return True


@celery.task(name='tasks.lookup_twitter_handle')
def lookup_twitter_handle(*args, **kwargs):
    print 'lookup_twitter_handle', args, kwargs
    return True


@celery.task(name='tasks.get_twitter_followers')
def get_twitter_followers(*args, **kwargs):
    print 'get_twitter_followers', args, kwargs
    return True


@celery.task(name='tasks.get_tweets')
def get_tweets(*args, **kwargs):
    print 'get_tweets', args, kwargs
    return True


@celery.task(name='tasks.download_charity_homepage')
def download_charity_homepage(*args, **kwargs):
    print 'download_charity_homepage', args, kwargs
    return True


@celery.task(name='tasks.download_charity_news')
def download_charity_news(*args, **kwargs):
    print 'download_charity_news', args, kwargs
    return True


@celery.task(name='tasks.process_ein')
def process_ein(ein):
    '''Add a new charity with the given ein. Launches asynchronous
    tasks. Return a GroupResult to monitor the success of each task if
    needed.'''
    # look up twitter handle then (get followers and get tweets in parallel)
    twitter_chain = chain(lookup_twitter_handle.s(),
                          group([get_twitter_followers.s(),
                                 get_tweets.s()])
                          )
    # do these three in parallel
    tasks = group([twitter_chain,
                   download_charity_news.s(),
                   download_charity_homepage.s()])

    # lookup guidestar info before doing anything else.
    return chain(guidestar.s(ein),
                 tasks
                 ).apply_async()


if __name__ == '__main__':
    print process_ein('52-1693387')  # WWF
