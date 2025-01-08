#ai_support_platform/routes/crm.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ai_support_platform.models import db, Customer
from ai_support_platform.schemas import CustomerSchema
from ai_support_platform.utils import get_customer_by_id, is_admin

crm_bp = Blueprint('crm', __name__)

@crm_bp.route('/customer/<int:id>', methods=['GET'])
@jwt_required()
def get_customer(id):
    """Fetch customer details by ID"""
    current_user = get_jwt_identity()
    
    # Check if user has permission (Admin or Customer themselves)
    customer = get_customer_by_id(id)
    if customer is None:
        return jsonify({"message": "Customer not found."}), 404
    
    if customer.id != current_user['id'] and not is_admin(current_user):
        return jsonify({"message": "Access forbidden."}), 403
    
    customer_schema = CustomerSchema()
    return jsonify(customer_schema.dump(customer))

@crm_bp.route('/customer/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    """Update customer information"""
    current_user = get_jwt_identity()
    
    # Check if user has permission (Admin or Customer themselves)
    customer = get_customer_by_id(id)
    if customer is None:
        return jsonify({"message": "Customer not found."}), 404
    
    if customer.id != current_user['id'] and not is_admin(current_user):
        return jsonify({"message": "Access forbidden."}), 403
    
    # Get the updated data from the request
    data = request.get_json()
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)
    customer.address = data.get('address', customer.address)

    db.session.commit()

    customer_schema = CustomerSchema()
    return jsonify(customer_schema.dump(customer))

@crm_bp.route('/customer', methods=['POST'])
@jwt_required()
def create_customer():
    """Create a new customer profile (Admin only)"""
    current_user = get_jwt_identity()

    if not is_admin(current_user):
        return jsonify({"message": "Access forbidden."}), 403

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')

    # Create the customer profile
    new_customer = Customer(name=name, email=email, phone=phone, address=address)
    db.session.add(new_customer)
    db.session.commit()

    customer_schema = CustomerSchema()
    return jsonify(customer_schema.dump(new_customer)), 201

@crm_bp.route('/customers', methods=['GET'])
@jwt_required()
def get_all_customers():
    """Fetch all customers (Admin only)"""
    current_user = get_jwt_identity()

    if not is_admin(current_user):
        return jsonify({"message": "Access forbidden."}), 403

    customers = Customer.query.all()
    customer_schema = CustomerSchema(many=True)
    return jsonify(customer_schema.dump(customers))

@crm_bp.route('/customer/history/<int:id>', methods=['GET'])
@jwt_required()
def get_customer_history(id):
    """Get the customer's interaction history"""
    current_user = get_jwt_identity()
    
    # Check if user has permission (Admin or Customer themselves)
    customer = get_customer_by_id(id)
    if customer is None:
        return jsonify({"message": "Customer not found."}), 404
    
    if customer.id != current_user['id'] and not is_admin(current_user):
        return jsonify({"message": "Access forbidden."}), 403

    # Assuming we have a model for customer interactions (e.g., Ticket or Call logs)
    interactions = customer.interactions.all()  # Example for fetching interactions
    return jsonify([interaction.to_dict() for interaction in interactions])

@crm_bp.route('/customer/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    """Delete a customer profile (Admin only)"""
    current_user = get_jwt_identity()

    if not is_admin(current_user):
        return jsonify({"message": "Access forbidden."}), 403

    customer = get_customer_by_id(id)
    if customer is None:
        return jsonify({"message": "Customer not found."}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted successfully."}), 200
