from flask import Blueprint, request, jsonify
from twilio.rest import Client

call_bp = Blueprint('call', __name__)

TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_number"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@call_bp.route("/make_call", methods=["POST"])
def make_call():
    data = request.json
    call = client.calls.create(
        twiml='<Response><Say>Hello, this is your support agent!</Say></Response>',
        to=data['to'],
        from_=TWILIO_PHONE_NUMBER
    )
    return jsonify({"message": "Call initiated", "call_sid": call.sid})
