from functools import wraps
from flask import jsonify
from flask_login import login_required, current_user

def role_required(*roles):
    def wrapper(func):
        @login_required
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'message': 'Login required'}), 401
            
            if 'admin' in roles and not current_user.is_admin:
                return jsonify({'message': 'Access forbidden: admin role required'}), 403

            return func(*args, **kwargs)
        return decorated_view
    return wrapper
