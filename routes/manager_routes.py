from flask import Blueprint, request, jsonify
from models.candidate import Candidate

manager_blueprint = Blueprint('manager', __name__)

# Get Shortlisted Candidates
@manager_blueprint.route('/candidates', methods=['GET'])
def get_shortlisted_candidates():
    candidates = Candidate.get_shortlisted()
    return jsonify(candidates), 200

# Send Test Invitation
@manager_blueprint.route('/send-test', methods=['POST'])
def send_test_invitation():
    data = request.json
    candidate_id = data["candidate_id"]
    test_link = data["test_link"]
    # Logic to send test invitation
    return jsonify({"message": "Test invitation sent"}), 200