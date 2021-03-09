from pymongo import MongoClient

from Config import env_dev


def connect_to_mongodb(col_name):
    try:
        client = MongoClient(host=env_dev.mongouri)
        db = client[env_dev.database]
        col = db[col_name]
        print("\n[MongoDB] \tConnected to MongoDB successfully, returning collection: {}".format(col_name))

        return col
    except Exception as ex:
        print(ex)
        exception_data = {'MONGO exception message': f'{ex}'}