import sys
import logging
import importlib

import pymongo
from pymongo import MongoClient

env = importlib.__import__("Config.env_" + sys.argv[1], fromlist=("env_" + sys.argv[1]))

try:
    client = MongoClient(host=env.mongo_uri)
    logging.log(level=logging.INFO, msg='Established connection to mongoDB')
except Exception as ex:
    exception_data = {'MongoDB exception': f'{ex}'}
    logging.log(level=logging.ERROR, msg=exception_data)
else:
    database = client[env.database]
    user_stats = database[env.col_users]
    server_stats = database[env.col_server]
    logging.log(level=logging.INFO, msg='Connected to Database and Collections')


def update_user_record(user_id: str, guild_id: str, practice_time: int, last_rep: str):
    if practice_time is not None:
        query = {'userId': user_id, 'guild_id': guild_id}
        pipeline = {'$set': {'info.practiceStats.lastRep': last_rep, 'info.practiceStats.lastRepTime': practice_time}, '$inc': {'info.practiceStats.totalTime': practice_time}}
        try:
            user_stats.update_one(filter=query, update=pipeline, upsert=True)
        except Exception as ex:
            update_exception = {'MongoDB exception': f'{ex}'}
            logging.log(level=logging.ERROR, msg=update_exception)
        else:
            logging.log(level=logging.INFO, msg=f'Successfully updated practice time in database for user {user_id} in guild {guild_id}')
    return


def find_user_record(user_id: str, guild_id: str):
    return user_stats.find_one({'userId': user_id, 'guild_id': guild_id})


def find_server_record(guild_id: str):
    return server_stats.find_one({'guild_id': guild_id})


def update_server_record(guild_id: str, practice_time: int):
    if practice_time is not None:
        query = {'guild_id': guild_id}
        pipeline = {
            '$inc': {
                'practiceStats.dailyTotal': practice_time,
                'practiceStats.weeklyTotal': practice_time,
                'practiceStats.monthlyTotal': practice_time,
                'practiceStats.yearlyTotal': practice_time,
                'practiceStats.grandTotal': practice_time
            }
        }
        server_stats.update_one(filter=query, update=pipeline, upsert=True)
        return


def reset_server_practice_time(guild_id: str, attribute: str):
    query = {'guild_id': guild_id}
    pipeline = {'$set': {f'practiceStats.{attribute}': 0}}
    server_stats.update_one(filter=query, update=pipeline, upsert=True)
    return


def leaderboard(guild_id: str):
    return user_stats.find({'guild_id': guild_id}).sort('info.practiceStats.totalTime', pymongo.DESCENDING).limit(10)
