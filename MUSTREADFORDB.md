# Database Implementation Guide for Calculator App

## Overview

This document provides instructions for implementing and setting up the database component of our Three-Tier Architecture Calculator application. As the database administrator, you'll be responsible for implementing the database operations that are currently placeholders in the codebase.

!THIS WAS MADE BY AN AI IAM NOT RESPONSIBLE FOR ANY MISTAKES  BECAUSE I STILL DIDN'T LEARN MYSQL 

## Requirements

- SQLite database (as specified in the codebase)
- Python with `sqlite3` and `bcrypt` libraries
- Basic knowledge of SQL and database operations

## Implementation Tasks

### 1. Complete the `db.py` Module

The `App/db.py` file contains placeholder functions that need to be implemented:

#### 1.1 Database Connection Function

```python
def get_db_connection():
    """
    Create a connection to the SQLite database
    Returns the connection object
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn
```

#### 1.2 Database Initialization

```python
def init_db():
    """
    Run the SQL script to create tables
    """
    conn = get_db_connection()
    
    # Read SQL script from file
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql/create_tables.sql'), 'r') as f:
        sql_script = f.read()
    
    # Execute the script
    conn.executescript(sql_script)
    conn.commit()
    conn.close()
```

#### 1.3 User Authentication Functions

```python
def register_user(username, password):
    """
    Register a new user
    Returns True if successful, False if username already exists
    """
    try:
        conn = get_db_connection()
        
        # Hash the password with bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert user into database
        conn.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, password_hash.decode('utf-8'))
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Username already exists (unique constraint violated)
        return False
    except Exception as e:
        print(f"Error in register_user: {e}")
        return False

def verify_user(username, password):
    """
    Verify user credentials
    Returns user_id if valid, None if invalid
    """
    conn = get_db_connection()
    user = conn.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return user['id']
    
    return None
```

#### 1.4 History Functions

```python
def add_calculation_to_history(user_id, operation, expression, result):
    """
    Add a calculation to user history
    Keep only the last 5 calculations per user
    """
    conn = get_db_connection()
    
    # Insert new calculation
    conn.execute(
        'INSERT INTO calculation_history (user_id, operation, expression, result) VALUES (?, ?, ?, ?)',
        (user_id, operation, expression, result)
    )
    
    # Get count of user's calculations
    count = conn.execute(
        'SELECT COUNT(*) as count FROM calculation_history WHERE user_id = ?',
        (user_id,)
    ).fetchone()['count']
    
    # Delete older calculations if more than 5 exist
    if count > 5:
        # Get IDs of calculations to keep (5 most recent)
        keep_ids = [row['id'] for row in conn.execute(
            'SELECT id FROM calculation_history WHERE user_id = ? ORDER BY created_at DESC LIMIT 5',
            (user_id,)
        ).fetchall()]
        
        # Delete all other calculations for this user
        if keep_ids:
            placeholders = ','.join(['?'] * len(keep_ids))
            conn.execute(
                f'DELETE FROM calculation_history WHERE user_id = ? AND id NOT IN ({placeholders})',
                (user_id, *keep_ids)
            )
    
    conn.commit()
    conn.close()
    return True

def get_user_history(user_id, limit=5):
    """
    Get user's calculation history
    Returns a list of the last 'limit' calculations
    """
    conn = get_db_connection()
    
    history = conn.execute(
        '''
        SELECT operation, expression, result 
        FROM calculation_history 
        WHERE user_id = ? 
        ORDER BY created_at DESC
        LIMIT ?
        ''',
        (user_id, limit)
    ).fetchall()
    
    # Convert to list of dictionaries
    result = [
        {
            'operation': item['operation'],
            'expression': item['expression'],
            'result': item['result']
        }
        for item in history
    ]
    
    conn.close()
    return result
```

### 2. Update Authentication Module

The `App/authentication.py` file needs to be updated to use the database functions instead of the dummy users dictionary:

```python
# Replace imports at the top
from flask import Blueprint, request, jsonify, session
from functools import wraps
import logging
from .db import register_user, verify_user, get_user_history, add_calculation_to_history

auth_bp = Blueprint('auth', __name__, url_prefix='/api/authentication')

# The login_required decorator can stay as is

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user_id = verify_user(username, password)
    
    if user_id:
        session['username'] = username
        session['user_id'] = user_id  # Store user_id in session
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
    username = session.get('username')
    user_id = session.get('user_id')
    
    history = get_user_history(user_id)
    
    return jsonify({"history": history})
```

### 3. Update Routes Module

The `App/routes.py` file needs to be updated to use the database functions for adding to history:

```python
# Add this import at the top
from .db import add_calculation_to_history

@bp.route('/calculate', methods=['POST'])
@login_required
def calculate():
    data = request.get_json()
    expr = data.get('expression')
    operation = data.get('operation')
    username = session.get('username')
    user_id = session.get('user_id')  # Get user_id from session

    try:
        result = None
        
        if operation == 'derivative':
            result = calculate_derivative(expr)
        elif operation == 'integral':
            result = calculate_integral(expr)
        elif operation == 'limit':
            x_val = data.get('x_value')
            result = calculate_limit(expr, float(x_val))
        elif operation == 'solve':
            result = solve_equation(expr)
        elif operation == 'function':
            result = apply_function(expr)
        else:
            return jsonify({'error': 'Invalid operation'}), 400

        # Add to user history using database function
        add_calculation_to_history(user_id, operation, expr, str(result))
        
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 4. Initialize Database in App Creation

Update the `App/__init__.py` file to initialize the database:

```python
from flask import Flask, send_from_directory
from .routes import bp
from .authentication import auth_bp
import os
import secrets
from .db import init_db  # Add this import

def create_app():
    app = Flask(__name__, static_folder='../static')
    
    # Configure session
    app.secret_key = secrets.token_hex(16)  # Generate a random secret key
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
    
    # Initialize database
    init_db()  # Add this line
    
    # Register bluepprints
    app.register_blueprint(bp)
    app.register_blueprint(auth_bp)
    
    # Routes remain the same...
    
    return app
```

## Database Structure

The database structure is defined in the `sql/create_tables.sql` file. It includes:

1. **users** table:
   - `id`: Primary key
   - `username`: Unique username
   - `password_hash`: Hashed password
   - `created_at`: Timestamp

2. **calculation_history** table:
   - `id`: Primary key
   - `user_id`: Foreign key to users table
   - `operation`: Type of calculation
   - `expression`: The expression calculated
   - `result`: The result of the calculation
   - `created_at`: Timestamp

## Testing the Integration

1. After implementing these changes, run the application:
   ```
   python run.py
   ```

2. Test user registration and login to ensure the database operations work correctly

3. Test calculations and verify that history is being saved and retrieved correctly

## Security Considerations

- Make sure the database file is not accessible from the web
- Ensure proper error handling for all database operations
- Use parameterized queries (as shown in the examples) to prevent SQL injection
- Use bcrypt for password hashing (already included in the implementation)

## Performance Considerations

- Consider adding more indexes if query performance becomes an issue
- Monitor database size, especially if many users are using the application
- Consider adding a periodic cleanup process for old history entries if needed

## Collaboration Process

1. Implement the database functions in `db.py`
2. Test them individually
3. Update the authentication and routes modules to use the database functions
4. Test the full application flow
5. Submit a pull request with your changes
6. Document any issues or considerations that arose during implementation