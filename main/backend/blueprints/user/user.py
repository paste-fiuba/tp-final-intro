from flask import session, jsonify
from functools import wraps
from db import get_connection

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'No autenticado'}), 401
        return f(*args, **kwargs)
    return decorated_function

def get_user_by_id(user_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Usuario WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                return {
                    'id': user['id'],
                    'username': user['username'],
                    'role': user['role'],
                    'email': user['email'],
                    'created_at': user['created_at'],
                }
            return None