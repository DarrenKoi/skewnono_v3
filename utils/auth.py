"""
Authentication and authorization utilities
"""
from flask import request, jsonify
from functools import wraps
import logging
import platform
import os

logger = logging.getLogger(__name__)

def is_development_environment():
    """
    Check if we're in development environment
    Returns True if running in development mode
    """
    # Check environment variable override
    env_override = os.environ.get('AUTH_MODE')
    if env_override == 'bypass':
        return True
    elif env_override == 'enforce':
        return False
    
    # Check if running in development mode based on platform
    node_name = platform.node().upper()
    if node_name.startswith('DESKTOP'):
        return True  # Home development environment
    
    # Check Flask debug mode
    if os.environ.get('FLASK_ENV') == 'development' or os.environ.get('FLASK_DEBUG') == '1':
        return True
    
    return False

def is_restricted_user(user_id):
    """
    Check if user should be restricted based on their ID
    Returns True if user ID starts with 'X' or 'x'
    """
    if not user_id:
        return False
    return user_id.lower().startswith('x')

def get_user_from_cookie():
    """
    Extract LASTUSER from cookies
    Returns the user ID or None if not found
    """
    return request.cookies.get('LASTUSER')

def check_user_access():
    """
    Check if current user has access to protected resources
    Returns tuple (has_access: bool, user_id: str)
    """
    # In development environment, bypass authentication
    if is_development_environment():
        logger.info("Development environment detected - bypassing authentication")
        return True, "dev_user"
    
    user_id = get_user_from_cookie()
    if not user_id:
        logger.warning("No LASTUSER cookie found in request")
        return False, None
    
    has_access = not is_restricted_user(user_id)
    if not has_access:
        logger.info(f"Access denied for restricted user: {user_id}")
    
    return has_access, user_id

def require_access(f):
    """
    Decorator to protect routes from restricted users
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        has_access, user_id = check_user_access()
        
        if not has_access:
            return jsonify({
                'error': 'Access denied',
                'message': 'You do not have permission to access this resource'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function