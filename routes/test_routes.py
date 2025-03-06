from flask import Blueprint, request, jsonify
from models.exam import Exam

test_blueprint = Blueprint('exam', __name__)

# Get Coding Test Questions
@test_blueprint.route('/questions', methods=['GET'])
def get_questions():
    questions = Exam.get_questions()
    return jsonify(questions), 200

# Submit Coding Test Answers
@test_blueprint.route('/submit', methods=['POST'])
def submit_answers():
    data = request.json
    candidate_id = data["candidate_id"]
    answers = data["answers"]
    # Logic to submit answers
    return jsonify({"message": "Answers submitted successfully"}), 200