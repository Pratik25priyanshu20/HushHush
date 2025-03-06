'''
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from config import SECRET_KEY
from utils import get_mongo_collection

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/register", methods=["POST"])
def register():
    """Register a new user (Candidate, Manager, or HR)."""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")  # Candidate, Manager, or HR

    collection = get_mongo_collection("mongodb://127.0.0.1:27017/", "Hiring_database", "users")

    if collection.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    collection.insert_one({"email": email, "password": hashed_password, "role": role})

    return jsonify({"message": f"{role} registered successfully!"}), 201

@auth_blueprint.route("/login", methods=["POST"])
def login():
    """Authenticate user and return JWT token."""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    collection = get_mongo_collection("mongodb://127.0.0.1:27017/", "Hiring_database", "users")
    user = collection.find_one({"email": email})

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({"email": email, "role": user["role"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)}, SECRET_KEY)
    
    return jsonify({"token": token})
    '''
    
    
from flask import Blueprint, request, jsonify
from models.candidate import Candidate
from models.manager import Manager
from models.hr import HR

auth_blueprint = Blueprint('auth', __name__)

# Candidate Registration
@auth_blueprint.route('/candidate/register', methods=['POST'])
def register_candidate():
    data = request.json
    candidate = Candidate(data)
    candidate.save()
    return jsonify({"message": "Candidate registered successfully"}), 201

# Candidate Login
@auth_blueprint.route('/candidate/login', methods=['POST'])
def login_candidate():
    data = request.json
    candidate = Candidate.find_by_email(data["email"])
    if candidate and candidate.verify_password(data["password"]):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Hiring Manager Login
@auth_blueprint.route('/manager/login', methods=['POST'])
def login_manager():
    data = request.json
    manager = Manager.find_by_email(data["email"])
    if manager and manager.verify_password(data["password"]):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# HR Login
@auth_blueprint.route('/hr/login', methods=['POST'])
def login_hr():
    data = request.json
    hr = HR.find_by_email(data["email"])
    if hr and hr.verify_password(data["password"]):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401