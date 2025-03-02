from pymongo import MongoClient
import datetime
import config

# MongoDB Connection
client = MongoClient(config.MONGO_URI)
db = client["hiring_system"]

# Ensure Collections Exist
users_collection = db["users"]
exams_collection = db["exams"]
submissions_collection = db["submissions"]

# Sample User Document
user_schema = {
    "name": "Example User",  # Full Name
    "email": "user@example.com",  # Unique Email
    "password": "hashed_password",  # Hashed Password
    "role": "candidate",  # candidate, manager, hr
    "created_at": datetime.datetime.utcnow()
}

# Sample Exam Document
exam_schema = {
    "candidate_email": "user@example.com",  # Candidate taking the exam
    "status": "Pending",  # Pending, Ongoing, Submitted, Passed, Failed
    "start_time": None,  # When the exam starts
    "submission_time": None,  # When submitted
    "questions": ["What is Python?", "Implement a linked list"],  # Sample questions
    "answers": {},  # Candidate's submitted answers
}

# Sample Submission Document
submission_schema = {
    "candidate_email": "user@example.com",  # Candidate who submitted
    "exam_id": "some_exam_id",  # Reference to exam
    "answers": {"Q1": "Python is...", "Q2": "class Node:"},  # Submitted answers
    "score": None,  # Score after evaluation
    "evaluated": False,  # Whether the exam has been checked
    "submission_time": datetime.datetime.utcnow()
}

# Insert Sample Data (Only if Collection is Empty)
if users_collection.count_documents({}) == 0:
    users_collection.insert_one(user_schema)
if exams_collection.count_documents({}) == 0:
    exams_collection.insert_one(exam_schema)
if submissions_collection.count_documents({}) == 0:
    submissions_collection.insert_one(submission_schema)
