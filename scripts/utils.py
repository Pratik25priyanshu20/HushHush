from pymongo import MongoClient

def get_mongo_collection(connection_string, db_name, collection_name):
    """
    Connect to MongoDB and return the specified collection.
    """
    try:
        # Connect to MongoDB
        client = MongoClient(connection_string)
        db = client[db_name]
        collection = db[collection_name]
        print(f"Connected to MongoDB: {db_name}.{collection_name}")
        return collection
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None