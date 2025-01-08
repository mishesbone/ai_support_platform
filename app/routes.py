from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Chat, Ticket, User, db
from datetime import datetime


# Define Blueprints
chat = Blueprint('chat', __name__)
call = Blueprint('call', __name__)
ticket = Blueprint('ticket', __name__)
crm = Blueprint('crm', __name__)
auth = Blueprint('auth', __name__)
dashboard = Blueprint('dashboard', __name__)

# Define routes for each blueprint

# Chat routes
@chat.route('/chat')
def some_chat_function():
    return  render_template('chat.html')

# Call routes
@call.route('/call')
def some_call_function():
    return  render_template('call.html')

# Ticket routes
@ticket.route('/ticket')
def some_ticket_function():
    return  render_template('ticket.html')

# CRM routes
@crm.route('/crm')
def some_crm_function():
    return  render_template('crm.html')

# Auth routes
@auth.route('/login')
def some_auth_function():
    return  render_template('login.html')

# Dashboard routes
@dashboard.route('/dashboard')
def some_dashboard_function():
    return  render_template('dashboard.html')

# Export the blueprints to be used in other parts of the app
__all__ = ['chat', 'call', 'ticket', 'crm', 'auth', 'dashboard']
