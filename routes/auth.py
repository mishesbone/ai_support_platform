#ai_support_platform/routes/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from app.models import User, db

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

# User registration route
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    # Create a new user
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# User login route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    # Validate user credentials
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    # Create JWT token
    access_token = create_access_token(identity={"id": user.id, "email": user.email})
    return jsonify({"access_token": access_token}), 200

# Get user profile (protected route)
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({
        "id": current_user["id"],
        "email": current_user["email"]
    })
