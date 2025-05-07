import psycopg2
import os
import bcrypt
from psycopg2 import sql
from config import Config

def get_db_connection():
    """Establish connection to PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        raise

def init_db():
    """Initialize database tables"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        
        sql_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql/create_tables.sql')
        with open(sql_path, 'r') as f:
            sql_script = f.read()
        
        
        cursor.execute(sql_script)
        conn.commit()
        print("Database tables created successfully")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            cursor.close()
            conn.close()

def register_user(username, password):
    """Register a new user with hashed password"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute(
            sql.SQL("INSERT INTO users (username, password_hash) VALUES (%s, %s)"),
            (username, password_hash.decode('utf-8'))
        )
        conn.commit()
        return True
    except psycopg2.IntegrityError:
        return False  # Username already exists
    except Exception as e:
        print(f"Error registering user: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()

def verify_user(username, password):
    """Verify user credentials"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            sql.SQL("SELECT id, password_hash FROM users WHERE username = %s"),
            (username,)
        )
        user = cursor.fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            return user[0]  # Return user ID
        return None
        
    except Exception as e:
        print(f"Error verifying user: {e}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

def add_calculation_to_history(user_id, operation, expression, result):
    """Add calculation to history and maintain only 5 most recent"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert new calculation
        cursor.execute(
            sql.SQL("""
                INSERT INTO calculation_history 
                (user_id, operation, expression, result) 
                VALUES (%s, %s, %s, %s)
            """),
            (user_id, operation, expression, result)
        )
        
        # Get count of calculations
        cursor.execute(
            sql.SQL("""
                SELECT COUNT(*) as count 
                FROM calculation_history 
                WHERE user_id = %s
            """),
            (user_id,)
        )
        count = cursor.fetchone()[0]
        
        # Keep only 5 most recent if over limit
        if count > 5:
            cursor.execute(
                sql.SQL("""
                    DELETE FROM calculation_history
                    WHERE id NOT IN (
                        SELECT id 
                        FROM calculation_history 
                        WHERE user_id = %s 
                        ORDER BY created_at DESC 
                        LIMIT 5
                    )
                    AND user_id = %s
                """),
                (user_id, user_id)
            )
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Error adding to history: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_user_history(user_id, limit=5):
    """Retrieve user's calculation history"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            sql.SQL("""
                SELECT operation, expression, result 
                FROM calculation_history 
                WHERE user_id = %s 
                ORDER BY created_at DESC
                LIMIT %s
            """),
            (user_id, limit)
        )
        
        history = cursor.fetchall()
        return [
            {
                'operation': item[0],
                'expression': item[1],
                'result': item[2]
            }
            for item in history
        ]
        
    except Exception as e:
        print(f"Error getting history: {e}")
        return []
    finally:
        if conn:
            cursor.close()
            conn.close()