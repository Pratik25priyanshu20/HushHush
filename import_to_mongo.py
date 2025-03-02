import json
import pymongo
from pymongo import MongoClient

# Path to your JSON file
json_file_path = '/Users/futurediary/Desktop/Projects/MongoDb/github_users_with_emails.json'

# Connect to MongoDB
# Default connection string for local MongoDB
client = MongoClient('mongodb://127.0.0.1:27017/')


db_name = 'Hiring_databse'  # Change to your preferred database name
collection_name = 'git_candidates'    

db = client[db_name]
collection = db[collection_name]

print(f"Loading data from: {json_file_path}")
with open(json_file_path, 'r') as file:
    data = json.load(file)

print(f"Data type: {type(data)}")
print(f"Number of records: {len(data) if isinstance(data, list) else 'Not a list'}")

# Insert data into MongoDB
if isinstance(data, list):
    result = collection.insert_many(data)
    print(f"Inserted {len(result.inserted_ids)} documents into {db_name}.{collection_name}")
else:
    try:
        result = collection.insert_one(data)
        print(f"Inserted 1 document into {db_name}.{collection_name}")
    except Exception as e:
        print(f"Error: {e}")
        print("Try converting your JSON to a list of records format.")

print(f"\nCollection '{collection_name}' stats:")
print(f"Total documents: {collection.count_documents({})}")

# Display sample document
print("\nSample document:")
sample = collection.find_one()
if sample:
    # Remove _id for cleaner output
    if '_id' in sample:
        sample['_id'] = str(sample['_id'])  # Convert ObjectId to string for display
    print(json.dumps(sample, indent=2))
