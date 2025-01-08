#ai_support_platform/routes/ticket.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Ticket, User, db
from datetime import datetime

ticket_bp = Blueprint('ticket', __name__, url_prefix="/ticket")

# Create a new ticket
@ticket_bp.route("/create", methods=["POST"])
@jwt_required()
def create_ticket():
    """
    Endpoint to create a new ticket.
    """
    try:
        current_user = get_jwt_identity()
        data = request.json

        new_ticket = Ticket(
            title=data['title'],
            description=data['description'],
            status="open",
            priority=data['priority'],
            user_id=current_user["id"],
            created_at=datetime.utcnow()
        )

        db.session.add(new_ticket)
        db.session.commit()

        return jsonify({"message": "Ticket created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get all tickets for the current user
@ticket_bp.route("/my_tickets", methods=["GET"])
@jwt_required()
def get_my_tickets():
    """
    Endpoint to fetch all tickets created by the current user.
    """
    try:
        current_user = get_jwt_identity()
        tickets = Ticket.query.filter_by(user_id=current_user["id"]).all()

        ticket_list = [
            {
                "id": ticket.id,
                "title": ticket.title,
                "description": ticket.description,
                "status": ticket.status,
                "priority": ticket.priority,
                "created_at": ticket.created_at,
                "updated_at": ticket.updated_at
            }
            for ticket in tickets
        ]

        return jsonify({"tickets": ticket_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update ticket status or priority
@ticket_bp.route("/update/<int:ticket_id>", methods=["PUT"])
@jwt_required()
def update_ticket(ticket_id):
    """
    Endpoint to update a ticket's status or priority.
    """
    try:
        data = request.json
        ticket = Ticket.query.get_or_404(ticket_id)

        # Update only the provided fields
        if "status" in data:
            ticket.status = data["status"]
        if "priority" in data:
            ticket.priority = data["priority"]

        ticket.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({"message": "Ticket updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a ticket
@ticket_bp.route("/delete/<int:ticket_id>", methods=["DELETE"])
@jwt_required()
def delete_ticket(ticket_id):
    """
    Endpoint to delete a ticket by its ID.
    """
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        db.session.delete(ticket)
        db.session.commit()

        return jsonify({"message": "Ticket deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
