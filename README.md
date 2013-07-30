givinggraph
========



## Configuration
Various API and Database credentials are read from a configuration file. A sample file is provided: `sample.cfg`. You should:

1. copy sample.cfg to somewhere else (e.g., ~/.giving)
2. add your credentials
3. set an environment GGRAPH_CFG to point to the file (e.g., `export GGRAPH_CFG ~/.giving`)


### Celery
givinggraph uses Celery to schedule asynchronous tasks (like web crawling, API calls, etc). Below, we first launch a celery worker, then run a script to test it out:

```
celery -A givinggraph.tasks worker --loglevel=INFO
python -m givinggraph.tasks
```

