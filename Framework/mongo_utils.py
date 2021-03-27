import importlib
import sys
from pymongo import MongoClient

env = importlib.__import__("Config.env_" + sys.argv[1], fromlist=("env_" + sys.argv[1]))


client = MongoClient(host=env.mongo_uri)

def connect_to_mongodb(col_name):
    try:
        db = client[env.database]
        col = db[col_name]
        print("\n[MongoDB] \tConnected to MongoDB successfully, returning collection: {}".format(col_name))

        return col
    except Exception as ex:
        print(ex)
        exception_data = {'MONGO exception message': f'{ex}'}




