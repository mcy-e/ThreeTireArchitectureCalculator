# App/auth.py
from flask import Blueprint, request, jsonify, session
from functools import wraps
import logging

auth_bp = Blueprint('auth', __name__, url_prefix='/api/authentication')

# TODO : 'replace by database operations'
DUMMY_USERS = {
    "user1": {"password": "password1", "history": []},
    "user2": {"password": "password2", "history": []}
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # TODO(for 7a9o): Replace with actual database lookup
    if username in DUMMY_USERS and DUMMY_USERS[username]["password"] == password:
        session['username'] = username
        return jsonify({"success": True, "message": f"Welcome, {username}!"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({"success": True, "message": "Logged out successfully"})

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    #*check if exists
    # TODO(for 7a9o): Replace with actual database check
    if username in DUMMY_USERS:
        return jsonify({"success": False, "message": "Username already exists"}), 400
    
    # TODO(for 7a9o): Replace with actual database insertion
    #* we just use the dummy to test
    DUMMY_USERS[username] = {"password": password, "history": []}
    
    return jsonify({"success": True, "message": "Registration successful"})

@auth_bp.route('/check', methods=['GET'])
def check_auth():
    if 'username' in session:
        return jsonify({"authenticated": True, "username": session['username']})
    else:
        return jsonify({"authenticated": False})

@auth_bp.route('/history', methods=['GET'])
@login_required
def get_history():
    username = session.get('username')
    
    # TODO(for 7a9o): Replace with actual database query
    history = DUMMY_USERS.get(username, {}).get("history", [])
    
    return jsonify({"history": history})

def add_to_history(username, operation, expression, result):
    """
    add a calculation to user history this would be replaced by database operations
    """
    # TODO (for 7a9o): Replace with actual database insertion
    if username in DUMMY_USERS:
        history_item = {
            "operation": operation,
            "expression": expression,
            "result": result
        }
        
        #* add operation in the list
        DUMMY_USERS[username]["history"].insert(0, history_item)
        
        #* keep the last 5 items
        if len(DUMMY_USERS[username]["history"]) > 5:
            DUMMY_USERS[username]["history"] = DUMMY_USERS[username]["history"][:5]
        
        return True
    return False