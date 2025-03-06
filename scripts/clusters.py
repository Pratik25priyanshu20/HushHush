from utils import get_mongo_collection
import pandas as pd
import numpy as np

def label_clusters():
    # MongoDB connection details
    connection_string = "mongodb://127.0.0.1:27017/"
    db_name = "Hiring_database"
    collection_name = "candidates"

    
    collection = get_mongo_collection(connection_string, db_name, collection_name)

    if collection is None:
        print("Failed to connect to MongoDB or collection does not exist.")
        return

    
    data = list(collection.find())
    df = pd.DataFrame(data)

    
    if df.empty:
        print("The DataFrame is empty. No data to process.")
        return

    
    if "label" in df.columns:
        print("Clusters are already labeled.")
        return

    
    features = [
        "followers", "public_repos", "top_repo_stars", "commits_last_year",
        "issues_participated", "pull_requests", "forked_repos"
    ]

    
    percentiles = {}
    for feature in features:
        percentiles[feature] = {
            "25th": np.percentile(df[feature], 25),
            "50th": np.percentile(df[feature], 50),
            "75th": np.percentile(df[feature], 75)
        }

    
    def assign_label(row):
        score = 0
        for feature in features:
            if row[feature] >= percentiles[feature]["75th"]:
                score += 2  # Good
            elif row[feature] >= percentiles[feature]["25th"]:
                score += 1  # Average
            else:
                score += 0  # Bad

        
        if score >= 10:  
            return "Good"
        elif score >= 5:
            return "Average"
        else:
            return "Bad"

    
    df["label"] = df.apply(assign_label, axis=1)

    
    for index, row in df.iterrows():
        collection.update_one({"_id": row["_id"]}, {"$set": {"label": row["label"]}})

    print("Clusters labeled and saved to MongoDB.")
label_clusters()