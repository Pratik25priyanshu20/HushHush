
from utils import get_mongo_collection
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def train_kmeans():
    # MongoDB connection details
    connection_string = "mongodb://127.0.0.1:27017/"
    db_name = "Hiring_databse"
    collection_name = "git_candidates"

    # Fetch collection
    collection = get_mongo_collection(connection_string, db_name, collection_name)

    # Check if collection is None (connection failed)
    if collection is None:
        print("Failed to connect to MongoDB or collection does not exist.")
        return

    # Fetch data from MongoDB
    data = list(collection.find())

    # Debug: Print the number of documents fetched
    print(f"Number of documents fetched: {len(data)}")

    # Check if data is empty
    if not data:
        print("The collection is empty. Please check your data.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Debug: Print the first few rows of the DataFrame
    print("First few rows of the DataFrame:")
    print(df.head())

    # Check if DataFrame is empty
    if df.empty:
        print("The DataFrame is empty. No data to process.")
        return

    # Features for clustering
    features = df[["repositories", "commits"]]

    # Debug: Print the shape of the features
    print(f"Shape of features: {features.shape}")

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=3, random_state=42)  # Adjust n_clusters as needed
    df["cluster"] = kmeans.fit_predict(features)

    # Visualize clusters
    plt.scatter(features["repositories"], features["commits"], c=df["cluster"], cmap="viridis")
    plt.xlabel("Repositories")
    plt.ylabel("Commits")
    plt.title("K-Means Clustering")
    plt.colorbar(label="Cluster")
    plt.show()

    # Save clusters back to MongoDB
    for index, row in df.iterrows():
        collection.update_one({"_id": row["_id"]}, {"$set": {"cluster": int(row["cluster"])}})

    print("Clustering completed and saved to MongoDB.")

# Run the function
train_kmeans()