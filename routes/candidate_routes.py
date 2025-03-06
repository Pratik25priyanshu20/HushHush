from flask import Blueprint, request, jsonify
from models.candidate import Candidate

candidate_blueprint = Blueprint('candidate', __name__)

# Get Candidate Profile
@candidate_blueprint.route('/profile', methods=['GET'])
def get_profile():
    candidate_id = request.args.get("candidate_id")
    candidate = Candidate.find_by_id(candidate_id)
    if candidate:
        return jsonify(candidate), 200
    return jsonify({"message": "Candidate not found"}), 404

# Get Test Status
@candidate_blueprint.route('/test-status', methods=['GET'])
def get_test_status():
    candidate_id = request.args.get("candidate_id")
    candidate = Candidate.find_by_id(candidate_id)
    if candidate:
        return jsonify({"status": candidate["status"]}), 200
    return jsonify({"message": "Candidate not found"}), 404