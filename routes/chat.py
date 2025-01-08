# app/routes/chat.py

from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Chat, Ticket
from flask import Blueprint, request, jsonify
from app import db

# Define the Blueprint
chat_bp = Blueprint('chat', __name__)

@chat_bp.route("/", methods=["POST"])  # Use chat_bp here
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


@chat_bp.route("/update/<int:chat_id>", methods=["PUT"])  # Use chat_bp here
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


@chat_bp.route("/", methods=["POST"])  # Use chat_bp here (this route seems duplicated, remove it if not needed)
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

@chat_bp.route("/<int:ticket_id>", methods=["GET"])  # Use chat_bp here
def get_chats(ticket_id):
    chats = Chat.query.filter_by(ticket_id=ticket_id).all()
    return jsonify([{"id": chat.id, "message": chat.message, "timestamp": chat.timestamp} for chat in chats])

@chat_bp.route("/<int:chat_id>", methods=["DELETE"])  # Use chat_bp here
def delete_chat(chat_id):
    chat = Chat.query.get(chat_id)
    db.session.delete(chat)
    db.session.commit()
    return jsonify({"message": "Chat message deleted"}), 200
