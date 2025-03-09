



from utils import get_mongo_collection
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import joblib

def train_kmeans():
    #
    connection_string = "mongodb://127.0.0.1:27017/"
    db_name = "Hiring_database"  
    collection_name = "candidates"

    
    
    collection = get_mongo_collection(connection_string, db_name, collection_name)

    if collection is None:
        print("Failed to connect to MongoDB or collection does not exist.")
        return


    data = list(collection.find())

  
    print(f"Number of documents fetched: {len(data)}")

    
    if not data:
        print("The collection is empty. Please check your data.")
        return

    df = pd.DataFrame(data)

    print("First few rows of the DataFrame:")
    print(df.head())

   
    if df.empty:
        print("The DataFrame is empty. No data to process.")
        return

    features = df[["followers", "public_repos", "top_repo_stars", "commits_last_year", "pull_requests", "issues_participated", "forked_repos"]]

    
    print(f"Shape of features: {features.shape}")

   
    kmeans = KMeans(n_clusters=3, random_state=42)  
    df["cluster"] = kmeans.fit_predict(features)

    
    plt.scatter(features["public_repos"], features["followers"], c=df["cluster"], cmap="viridis")
    plt.xlabel("Public Repositories")
    plt.ylabel("Followers")
    plt.title("K-Means Clustering")
    plt.colorbar(label="Cluster")
    plt.show()

   
    for index, row in df.iterrows():
        collection.update_one({"_id": row["_id"]}, {"$set": {"cluster": int(row["cluster"])}})

    models_dir = "models"
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    model_path = os.path.join(models_dir, "kmeans_model.pkl")
    joblib.dump(kmeans, model_path)
    print(f"\n🎯 K-Means model saved to: {model_path}")

if __name__ == "__main__":
    train_kmeans()


