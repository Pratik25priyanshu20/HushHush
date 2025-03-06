'''
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

import os
from utils import get_mongo_collection
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, classification_report
import joblib

def train_random_forest():
   
    connection_string = "mongodb://127.0.0.1:27017/"
    db_name = "Hiring_databse"  
    collection_name = "git_candidates"

    # Fetch collection
    collection = get_mongo_collection(connection_string, db_name, collection_name)

    if collection is None:
        print(" Failed to connect to MongoDB or collection does not exist.")
        return

    # Fetch data from MongoDB
    data = list(collection.find({}, {"_id": 0})) 
    df = pd.DataFrame(data)

   
    if df.empty:
        print("⚠️ The DataFrame is empty. No data to process.")
        return

    required_features = ["repositories", "commits", "label"]
    missing_features = [feature for feature in required_features if feature not in df.columns]

    if missing_features:
        print(f" Missing required columns: {missing_features}. Please ensure the dataset is labeled correctly.")
        return

   
    X = df[["repositories", "commits"]]  
    y = df["label"]  

    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = RandomForestClassifier(
        n_estimators=50,  
        max_depth=5,  
        min_samples_split=20,
        min_samples_leaf=10,
        max_features="sqrt",
        bootstrap=True,
        random_state=42
    )
    
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate model performance
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted") 
    report = classification_report(y_test, y_pred)

   
    print("\n🔹 Model Performance Metrics:")
    print(f"✅ Accuracy: {accuracy:.4f}")
    print(f"✅ Precision: {precision:.4f}")
    print("\n📊 Classification Report:")
    print(report)
    
    train_accuracy = model.score(X_train, y_train)
    
    test_accuracy = model.score(X_test, y_test)
    print(f"✅ Train Accuracy: {train_accuracy:.4f}")
    print(f"✅ Test Accuracy: {test_accuracy:.4f}")

    
    

    # Save the model
    models_dir = "models"
    if not os.path.exists(models_dir):
        os.makedirs(models_dir) 

    model_path = os.path.join(models_dir, "random_forest_model.pkl")
    joblib.dump(model, model_path)
    print(f"\n🎯 Random Forest model saved to: {model_path}")


if __name__ == "__main__":
    train_random_forest() 
    '''
    
    
from utils import get_mongo_collection
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE  
import joblib
import os

def train_random_forest():
    
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

   
    features = df[["followers", "public_repos", "top_repo_stars", "commits_last_year", "pull_requests", "issues_participated", "forked_repos"]]
    target = df["label"]

    
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42, stratify=target)

    
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

    
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'bootstrap': [True, False]
    }

    
    rf = RandomForestClassifier(class_weight='balanced', random_state=42)

    
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)

    
    grid_search.fit(X_train_resampled, y_train_resampled)

    
    best_model = grid_search.best_estimator_

    
    y_pred = best_model.predict(X_test)

    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted")
    report = classification_report(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)

    
    print("\n🔹 Model Performance Metrics:")
    print(f"✅ Accuracy: {accuracy:.4f}")
    print(f"✅ Precision: {precision:.4f}")
    print("\n📊 Classification Report:")
    print(report)
    print("\n📊 Confusion Matrix:")
    print(conf_matrix)

    
    models_dir = "models"
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    model_path = os.path.join(models_dir, "random_forest_model.pkl")
    joblib.dump(best_model, model_path)
    print(f"\n🎯 Random Forest model saved to: {model_path}")

if __name__ == "__main__":
    train_random_forest()