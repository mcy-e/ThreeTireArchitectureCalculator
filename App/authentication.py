from flask import Blueprint, request, jsonify, session
from functools import wraps
from .db import register_user, verify_user, get_user_history

auth_bp = Blueprint('auth', __name__, url_prefix='/api/authentication')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user_id = verify_user(username, password)
    if user_id:
        session['username'] = username
        session['user_id'] = user_id
        return jsonify({"success": True, "message": f"Welcome, {username}!"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if register_user(username, password):
        return jsonify({"success": True, "message": "Registration successful"})
    else:
        return jsonify({"success": False, "message": "Username already exists"}), 400

@auth_bp.route('/history', methods=['GET'])
@login_required
def get_history():
    user_id = session.get('user_id')
    history = get_user_history(user_id)
    return jsonify({"history": history})

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return jsonify({"success": True, "message": "Logged out successfully"})