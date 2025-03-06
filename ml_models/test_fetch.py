from utils import get_mongo_collection
import pandas as pd

def check_class_distribution():
    # MongoDB connection details
    connection_string = "mongodb://127.0.0.1:27017/"
    db_name = "Hiring_database"
    collection_name = "candidates"  # Collection used for training

    # Fetch collection
    collection = get_mongo_collection(connection_string, db_name, collection_name)

    if collection is None:
        print("Failed to connect to MongoDB or collection does not exist.")
        return

    # Fetch data from MongoDB
    data = list(collection.find())
    df = pd.DataFrame(data)

    # Check class distribution
    class_distribution = df["label"].value_counts()
    print("Class Distribution:")
    print(class_distribution)

if __name__ == "__main__":
    check_class_distribution()