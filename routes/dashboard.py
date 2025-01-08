# ai_support_platform/routes/dashboard.py

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models import User, Ticket, db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix="/dashboard")

@dashboard_bp.route("/summary", methods=["GET"])
@jwt_required()
def get_summary():
    """
    Fetch dashboard summary statistics including:
    - Total users
    - Total tickets
    - Tickets by status
    """
    try:
        total_users = User.query.count()
        total_tickets = Ticket.query.count()
        
        # Tickets by status
        tickets_status = {
            "open": Ticket.query.filter_by(status="open").count(),
            "in_progress": Ticket.query.filter_by(status="in_progress").count(),
            "resolved": Ticket.query.filter_by(status="resolved").count(),
            "closed": Ticket.query.filter_by(status="closed").count()
        }

        return jsonify({
            "total_users": total_users,
            "total_tickets": total_tickets,
            "tickets_status": tickets_status
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dashboard_bp.route("/user_activity", methods=["GET"])
@jwt_required()
def get_user_activity():
    """
    Fetch user activity details:
    - Most active users
    - Recently registered users
    """
    try:
        # Example query for most active users (e.g., number of tickets created)
        most_active_users = User.query.join(Ticket).group_by(User.id).order_by(
            db.func.count(Ticket.id).desc()
        ).limit(5).all()

        active_users = [
            {"username": user.username, "email": user.email, "ticket_count": len(user.tickets)}
            for user in most_active_users
        ]

        # Recently registered users
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        recent_users_list = [
            {"username": user.username, "email": user.email, "registered_at": user.created_at}
            for user in recent_users
        ]

        return jsonify({
            "most_active_users": active_users,
            "recently_registered_users": recent_users_list
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
