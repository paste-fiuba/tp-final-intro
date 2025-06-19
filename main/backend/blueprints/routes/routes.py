from flask import Blueprint, request, jsonify, session
import datetime
import jwt
from config import SECRET_KEY

from blueprints.auth.auth import user_exists, create_user, check_password_hash, email_exists, get_user_by_username_and_email
from blueprints.admin.admin import jwt_admin_required
from blueprints.user.user import login_required, get_user_by_id

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({'success': False, 'message': 'Faltan datos'}), 400
    if user_exists(username):
        return jsonify({'success': False, 'message': 'Usuario ya registrado'}), 400
    if email_exists(email):
        return jsonify({'success': False, 'message': 'Email ya registrado'}), 400

    create_user(username, password, email)
    return jsonify({'message': 'Usuario creado exitosamente'}), 201

@usuarios_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json() if request.is_json else request.form

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Faltan datos'}), 400

    user = get_user_by_username_and_email(username, email)
    if not user:
        return jsonify({'message': 'Usuario o email incorrecto'}), 404

    if not check_password_hash(user["password_"], password):
        return jsonify({'message': 'Contraseña incorrecta'}), 401

    token_payload = {
        'user_id': user['id'],
        'username': user['username'],
        'role': user['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')

    return jsonify({
        'message': 'Inicio de sesión exitoso',
        'user_id': user['id'],
        'username': user['username'],
        'role': user['role'],
        'token': token
    }), 200

@usuarios_bp.route('/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Sesión cerrada exitosamente'}), 200

@usuarios_bp.route('/user/profile', methods=['GET'])
@login_required
def profile():
    user_id = session["user_id"]
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    
@usuarios_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id_endpoint(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

@usuarios_bp.route('/admin/dashboard', methods=['GET'])
@jwt_admin_required
def dashboard():
    return jsonify({'message': f'Panel de administración para el usuario con ID {session["user_id"]}'}), 200

@usuarios_bp.route('/admin/create_admin', methods=['POST'])
@jwt_admin_required
def create_admin_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password:
        return jsonify({'message': 'Faltan datos'}), 400
    if user_exists(username):
        return jsonify({'message': 'Usuario ya existente'}), 400
    create_user(username, password, email=email, role='admin')
    return jsonify({'message': 'Administrador creado exitosamente'}), 201

@usuarios_bp.route('/auth/status', methods=['GET'])
def session_status():
    if 'user_id' in session:
        return jsonify({'authenticated': True, 'user_id': session['user_id'], 'is_admin': session.get('is_admin', False)})
    return jsonify({'authenticated': False}), 200



