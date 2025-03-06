from pymongo import MongoClient

def get_mongo_collection(connection_string, db_name, collection_name):
    """Connect to MongoDB and return a collection."""
    try:
        client = MongoClient(connection_string)
        db = client[db_name]
        return db[collection_name]
    except Exception as e:
        print(f"MongoDB Connection Error: {e}")
        return None