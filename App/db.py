import sqlite3
import os
import bcrypt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql/create_tables.sql'), 'r') as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    conn.commit()
    conn.close()

def register_user(username, password):
    try:
        conn = get_db_connection()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        conn.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, password_hash.decode('utf-8'))
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"Error in register_user: {e}")
        return False

def verify_user(username, password):
    conn = get_db_connection()
    user = conn.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return user['id']
    return None

def add_calculation_to_history(user_id, operation, expression, result):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO calculation_history (user_id, operation, expression, result) VALUES (?, ?, ?, ?)',
        (user_id, operation, expression, result)
    )

    count = conn.execute(
        'SELECT COUNT(*) as count FROM calculation_history WHERE user_id = ?',
        (user_id,)
    ).fetchone()['count']

    if count > 5:
        keep_ids = [row['id'] for row in conn.execute(
            'SELECT id FROM calculation_history WHERE user_id = ? ORDER BY created_at DESC LIMIT 5',
            (user_id,)
        ).fetchall()]

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
