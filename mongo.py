from pymongo import MongoClient
import json


# Connect to your local MongoDB
client = MongoClient("mongodb://127.0.0.1:27017")

# Create or access a database
db = client["hiring_databse"]

# Create or access a collection
collection = db["git_candidates"]



# Load JSON data
with open("/Users/futurediary/Desktop/Projects/MongoDb/github_users_with_emails.json", "r") as file:
    data = json.load(file)

# Insert into MongoDB
if isinstance(data, list):  # If JSON file contains a list of dictionaries
    collection.insert_many(data)
else:  # If it's a single dictionary
    collection.insert_one(data)

print("JSON data inserted successfully!")