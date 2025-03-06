from flask import Blueprint, request, jsonify
from utils.mongo import get_mongo_collection
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email_blueprint = Blueprint('email', __name__)

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@example.com"
SENDER_PASSWORD = "your_password"

def send_email(recipient, subject, body):
    """
    Send an email to the recipient.
    """
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@email_blueprint.route('/send-selected', methods=['POST'])
def send_email_to_selected():
    # Fetch candidates with selection_status = "selected"
    collection = get_mongo_collection("candidates")
    selected_candidates = list(collection.find({"selection_status": "selected"}))

    if not selected_candidates:
        return jsonify({"message": "No selected candidates found"}), 404

    # Email details
    subject = "Coding Test Invitation"
    body = """
    Hi {name},

    You have been selected for a coding test. Please complete the test within 48 hours.

    Best regards,
    Hiring Team
    """

    # Send emails to selected candidates
    for candidate in selected_candidates:
        email_body = body.format(name=candidate["username"])
        success = send_email(candidate["email"], subject, email_body)
        if not success:
            return jsonify({"message": f"Failed to send email to {candidate['email']}"}), 500

    return jsonify({"message": "Emails sent successfully to selected candidates"}), 200