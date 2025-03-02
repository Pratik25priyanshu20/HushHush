from utils import get_mongo_collection

def label_clusters():
    # MongoDB connection details
    connection_string = "mongodb://127.0.0.1:27017/"
    db_name = "Hiring_databse"
    collection_name = "git_candidates"

    # Fetch collection
    collection = get_mongo_collection(connection_string, db_name, collection_name)

    if collection is None:
        print("Failed to connect to MongoDB or collection does not exist.")
        return

    # Define cluster labels
    cluster_labels = {0: "Good", 1: "Average", 2: "Poor"}

    # Update documents with cluster labels
    for cluster_num, label in cluster_labels.items():
        collection.update_many({"cluster": cluster_num}, {"$set": {"label": label}})

    print("Cluster labels updated in MongoDB.")

# Run the function
label_clusters()