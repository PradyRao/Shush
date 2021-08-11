import sys
import importlib

from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from Framework import mongo_utils

env = importlib.__import__("Config.env_" + sys.argv[1], fromlist=("env_" + sys.argv[1]))

jobstores = {
    'default': MongoDBJobStore(database=env.database, collection=env.cron_job_store, client=mongo_utils.client)
}
executors = {
    'default': ThreadPoolExecutor(5),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BlockingScheduler(standalone=True, executors=executors, job_defaults=job_defaults, timezone='Etc/GMT-5', daemon=True)
