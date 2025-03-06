from pymongo import MongoClient

def get_mongo_collection(collection_name):
    """
    Connect to MongoDB and return the specified collection.
    """
    connection_string = "mongodb://127.0.0.1:27017/"
    db_name = "hiring_system"
    client = MongoClient(connection_string)
    db = client[db_name]
    return db[collection_name]