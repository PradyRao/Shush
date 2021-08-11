import logging
from datetime import datetime, timedelta, timezone

from Framework import scheduler_utils
from Framework import mongo_utils


'''@scheduler_utils.scheduler.scheduled_job(trigger='cron', second='*/2', id='print_test')
def print_test():
    print(datetime.now().astimezone(timezone(timedelta(hours=-5))).isoformat())
    #mongo_utils.reset_server_practice_time_batch('dailyTotal')

@scheduler_utils.scheduler.scheduled_job(trigger='cron', second='*/2', id='print_test2')
def print_test():
    print("haihai " + datetime.now().astimezone(timezone(timedelta(hours=-5))).isoformat())'''


@scheduler_utils.scheduler.scheduled_job(trigger='cron', second='0', minute='0', hour='0', day='*', week='*', month='*',
                                         year='*', id='reset_daily')
def reset_daily():
    mongo_utils.reset_server_practice_time_batch('dailyTotal')


@scheduler_utils.scheduler.scheduled_job(trigger='cron', second='0', minute='0', hour='0', day_of_week=0, week='*',
                                         month='*', year='*', id='reset_weekly')
def reset_weekly():
    mongo_utils.reset_server_practice_time_batch('weeklyTotal')


@scheduler_utils.scheduler.scheduled_job(trigger='cron', second='0', minute='0', hour='0', day='1', month='*', year='*',
                                         id='reset_monthly')
def reset_monthly():
    mongo_utils.reset_server_practice_time_batch('monthlyTotal')


@scheduler_utils.scheduler.scheduled_job(trigger='cron', second='0', minute='0', hour='0', day='1', month='1', year='*',
                                         id='reset_yearly')
def reset_yearly():
    mongo_utils.reset_server_practice_time_batch('yearlyTotal')
