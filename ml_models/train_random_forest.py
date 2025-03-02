import os
from utils import get_mongo_collection
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, classification_report
import joblib

def train_random_forest():
    # MongoDB connection details
    connection_string = "mongodb://127.0.0.1:27017/"
    db_name = "Hiring_databse"
    collection_name = "git_candidates"

    # Fetch collection
    collection = get_mongo_collection(connection_string, db_name, collection_name)

    if collection is None:
        print("Failed to connect to MongoDB or collection does not exist.")
        return

    # Fetch data from MongoDB
    data = list(collection.find())
    df = pd.DataFrame(data)

    # Check if the DataFrame is empty
    if df.empty:
        print("The DataFrame is empty. No data to process.")
        return

    # Features and target
    features = df[["repositories", "commits"]]  # Use relevant features
    target = df["label"]  # Use the labeled clusters (e.g., "Good", "Average", "Poor")

    # Check if the target column exists
    if "label" not in df.columns:
        print("The 'label' column does not exist. Please label the clusters first.")
        return

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Train Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate model performance
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted")  # Use weighted average for multi-class
    report = classification_report(y_test, y_pred)

    # Print evaluation metrics
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print("Classification Report:")
    print(report)

    # Save the model
    models_dir = "models"
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)  # Create the directory if it doesn't exist

    model_path = os.path.join(models_dir, "random_forest_model.pkl")
    joblib.dump(model, model_path)
    print(f"Random Forest model saved to {model_path}")

# Run the function
train_random_forest()