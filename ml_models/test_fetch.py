from pymongo import MongoClient
import pandas as pd

# MongoDB connection
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["Hiring_databse"]
collection = db["git_candidates"]

# Fetch data
data = list(collection.find())

if not data:
    print("No data found in the collection.")
else:
    df = pd.DataFrame(data)
    print(f"Fetched {len(df)} documents.")
    print(df.head())