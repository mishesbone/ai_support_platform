# Import all the blueprints defined in app/routes.py
from .chat import chat
from .call import call
from .ticket import ticket
from .crm import crm
from .auth import auth
from .dashboard import dashboard

# Export all blueprints to be used in other parts of the application
__all__ = ['chat', 'call', 'ticket', 'crm', 'auth', 'dashboard']
