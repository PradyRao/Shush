import sys
import logging
import importlib

import pymongo
from pymongo import MongoClient

env = importlib.__import__("Config.env_" + sys.argv[1], fromlist=("env_" + sys.argv[1]))

# initialize the mongo client at startup
try:
    client = MongoClient(host=env.mongo_uri)
    logging.log(level=logging.INFO, msg='Established connection to mongoDB')
except Exception as ex:
    exception_data = {'MongoDB exception': f'{ex}'}
    logging.log(level=logging.ERROR, msg=exception_data)
else:
    # make connections to the database and relevant collections within that database
    database = client[env.database]
    user_stats_collection = database[env.col_users]
    server_stats_collection = database[env.col_server]
    channel_configuration_collection = database[env.col_channel_config]
    logging.log(level=logging.INFO, msg='Connected to Database and Collections')


# for stats command
# gets the practice record for a user
def find_user_record(user_id: str, guild_id: str):
    try:
        user_record = user_stats_collection.find_one({'userId': user_id, 'guild_id': guild_id})
    except Exception as ex:
        update_exception = {'MongoDB exception': f'{ex}'}
        logging.log(level=logging.ERROR, msg=update_exception)
        return None
    else:
        logging.log(level=logging.INFO, msg=f'Successfully retrieved stats for user {user_id} for guild {guild_id}')
        return user_record


# for serverstats
# gets the practice record for the server
def find_server_record(guild_id: str):
    try:
        server_record = server_stats_collection.find_one({'guild_id': guild_id})
    except Exception as ex:
        update_exception = {'MongoDB exception': f'{ex}'}
        logging.log(level=logging.ERROR, msg=update_exception)
        return None
    else:
        logging.log(level=logging.INFO, msg=f'Successfully retrieved stats for guild {guild_id}')
        return server_record


# this occurs when a practicing user leaves or ends their session
# takes the practice time and last rep of the user and updates it on the database
def update_user_record(user_id: str, guild_id: str, practice_time: int, last_rep: str):
    if practice_time is not None:
        query = {'userId': user_id, 'guild_id': guild_id}
        pipeline = {'$set': {'info.practiceStats.lastRep': last_rep, 'info.practiceStats.lastRepTime': practice_time},
                    '$inc': {'info.practiceStats.totalTime': practice_time}}
        try:
            user_stats_collection.update_one(filter=query, update=pipeline, upsert=True)
        except Exception as ex:
            update_exception = {'MongoDB exception': f'{ex}'}
            logging.log(level=logging.ERROR, msg=update_exception)
        else:
            logging.log(level=logging.INFO,
                        msg=f'Successfully updated practice time in database for user {user_id} in guild {guild_id}')
    return


# this occurs when any/every practicing users leave or end their session
# takes practice time updates it on the database
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
        try:
            server_stats_collection.update_one(filter=query, update=pipeline, upsert=True)
        except Exception as ex:
            update_exception = {'MongoDB exception': f'{ex}'}
            logging.log(level=logging.ERROR, msg=update_exception)
        else:
            logging.log(level=logging.INFO, msg=f'Successfully updated practice time in database for guild {guild_id}')
    return


# this will be used as a cron to periodically reset the an attribute for the server record
def reset_server_practice_time(guild_id: str, attribute: str):
    query = {'guild_id': guild_id}
    pipeline = {'$set': {f'practiceStats.{attribute}': 0}}
    try:
        server_stats_collection.update_one(filter=query, update=pipeline, upsert=True)
    except Exception as ex:
        update_exception = {'MongoDB exception': f'{ex}'}
        logging.log(level=logging.ERROR, msg=update_exception)
    else:
        logging.log(level=logging.INFO, msg=f'Successfully reset practice time for {attribute} in guild {guild_id}')
    return


def reset_server_practice_time_batch(attribute: str):
    pipeline = {'$set': {f'practiceStats.{attribute}': 0}}
    try:
        server_stats_collection.update_many(filter={}, update=pipeline, upsert=True)
    except Exception as ex:
        update_exception = {'MongoDB exception': f'{ex}'}
        logging.log(level=logging.ERROR, msg=update_exception)
    else:
        logging.log(level=logging.INFO, msg=f'Successfully reset practice time for {attribute}')
    return


# return stats documents sorted in total practice time descending order and limit it to 10 records
# returns the stats for users that have practiced the most in requested server
def get_user_leaderboard(guild_id: str):
    try:
        leaderboard = user_stats_collection.find({'guild_id': guild_id}).sort('info.practiceStats.totalTime',
                                                                              pymongo.DESCENDING).limit(10)
    except Exception as ex:
        update_exception = {'MongoDB exception': f'{ex}'}
        logging.log(level=logging.ERROR, msg=update_exception)
        return None
    else:
        logging.log(level=logging.INFO, msg=f'Successfully retrieved user leaderboard for guild {guild_id}')
        return leaderboard


# gets the requested server's current channel configurations
def get_channel_configurations(guild_id: str):
    try:
        channel_configurations = channel_configuration_collection.find_one({'guild_id': guild_id})
    except Exception as ex:
        update_exception = {'MongoDB exception': f'{ex}'}
        logging.log(level=logging.ERROR, msg=update_exception)
        return None
    else:
        logging.log(level=logging.INFO, msg=f'Successfully retrieved all channel configurations for guild {guild_id}')
        return channel_configurations


# updates requested server's current channel configurations
# essentially a cache sync - replaces the cloud configuration with the local cache
def update_channel_configurations(guild_id: str, applied_chs, broadcast_chs):
    query = {'guild_id': guild_id}
    pipeline = {'$set': {'applied_channels': applied_chs, 'broadcast_channels': broadcast_chs}}
    try:
        channel_configuration_collection.update_one(filter=query, update=pipeline, upsert=True)
    except Exception as ex:
        update_exception = {'MongoDB exception': f'{ex}'}
        logging.log(level=logging.ERROR, msg=update_exception)
    else:
        logging.log(level=logging.INFO, msg=f'Successfully updated channel configuration for guild {guild_id}')
    return


# occurs when the bot gets removed from a server
# deletes the entire document in collection corresponding that specific server
def delete_channel_configuration(guild_id: str):
    try:
        channel_configuration_collection.delete_one({'guild_id': guild_id})
    except Exception as ex:
        update_exception = {'MongoDB exception': f'{ex}'}
        logging.log(level=logging.ERROR, msg=update_exception)
    else:
        logging.log(level=logging.INFO, msg=f'Successfully deleted channel configuration for guild {guild_id}')
    return
