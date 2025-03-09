import os
import pandas as pd
import joblib
from utils import get_mongo_collection

def predict_candidates():
    
    
    connection_string = "mongodb://127.0.0.1:27017/"
    db_name = "Hiring_database"
    collection_name = "new_candidates"  

   
    collection = get_mongo_collection(connection_string, db_name, collection_name)

    if collection is None:
        print("Failed to connect to MongoDB or collection does not exist.")
        return

   
    data = list(collection.find({"technologies": {"$regex": "Python", "$options": "i"}}))

    if not data:
        print(" No candidates found with 'Python' in Technologies.")
        return

    df = pd.DataFrame(data)

    if df.empty:
        print(" The DataFrame is empty. No new candidates to process.")
        return

    
    required_features = ["followers", "public_repos", "top_repo_stars", "commits_last_year", "pull_requests", "issues_participated", "forked_repos"]

    if not all(feature in df.columns for feature in required_features):
        print(f" Missing required features: {set(required_features) - set(df.columns)}")
        return

    features = df[required_features]

    
    models_dir = "models"
    model_path = os.path.join(models_dir, "random_forest_model.pkl")

    if not os.path.exists(model_path):
        print(" Trained model not found. Please train the model first.")
        return

    model = joblib.load(model_path)

    
    predictions = model.predict(features)

    
    df["predicted_label"] = predictions
    df["selection_status"] = df["predicted_label"].apply(lambda x: "Selected" if x == "Good" else "Not Selected")

    
    for index, row in df.iterrows():
        collection.update_one(
            {"_id": row["_id"]},
            {"$set": {"predicted_label": row["predicted_label"], "selection_status": row["selection_status"]}}
        )

    print(f"✅ Predictions completed and saved for {len(df)} candidates who have Python in their Technologies.")

if __name__ == "__main__":
    predict_candidates()
    
    
