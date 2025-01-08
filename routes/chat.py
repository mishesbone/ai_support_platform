# This file contains the routes for the chat feature of the application.
# The routes are protected with JWT authentication.

#routes/chat.py

from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Chat, Ticket
from app.routes import bp
from flask import jsonify, request

@bp.route("/", methods=["POST"])
@jwt_required()
def send_message():
    data = request.json
    new_chat = Chat(
        message=data['message'],
        user_id=data['user_id'],
        ticket_id=data['ticket_id']
    )
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({"message": "Chat message sent"}), 201





@bp.route("/update/<int:chat_id>", methods=["PUT"])
@jwt_required()
def update_chat(chat_id):
    data = request.json
    chat = Chat.query.get(chat_id)
    if not chat:
        return jsonify({"message": "Chat message not found"}), 404
    
    current_user = get_jwt_identity()
    if chat.user_id != current_user:
        return jsonify({"message": "Unauthorized to update this chat message"}), 403
    
    chat.message = data['message']
    db.session.commit()
    return jsonify({"message": "Chat message updated"}), 200


from flask import Blueprint, request, jsonify
from app.models import Chat, db

bp = Blueprint('chat', __name__)

@bp.route("/", methods=["POST"])
def send_message():
    data = request.json
    new_chat = Chat(
        message=data['message'],
        user_id=data['user_id'],
        ticket_id=data['ticket_id']
    )
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({"message": "Chat message sent"}), 201

@bp.route("/<int:ticket_id>", methods=["GET"])
def get_chats(ticket_id):
    chats = Chat.query.filter_by(ticket_id=ticket_id).all()
    return jsonify([{"id": chat.id, "message": chat.message, "timestamp": chat.timestamp} for chat in chats])

@bp.route("/<int:chat_id>", methods=["DELETE"])
def delete_chat(chat_id):
    chat = Chat.query.get(chat_id)
    db.session.delete(chat)
    db.session.commit()
    return jsonify({"message": "Chat message deleted"}), 200

