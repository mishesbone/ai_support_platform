from flask import Blueprint, request, jsonify
from flask_mail import Mail, Message

email_bp = Blueprint('email', __name__)
mail = Mail()

@email_bp.route("/send_email", methods=["POST"])
def send_email():
    data = request.json
    msg = Message(
        subject=data['subject'],
        sender="support@yourdomain.com",
        recipients=[data['to']],
        body=data['message']
    )
    mail.send(msg)
    return jsonify({"message": "Email sent successfully"})
