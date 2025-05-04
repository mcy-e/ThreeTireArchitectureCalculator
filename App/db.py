import sqlite3
import os
import bcrypt

# TODO: every commented function is for 7a9o to implement

#*DB setup
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'calculator.db')

def get_db_connection():
    """
    create a connection to the SQLite database
    returns the connection object
    """
    # TODO: Implement this function
    pass

def init_db():
    """
    run the SQL script
    """
    # TODO: Implement this function
    #* read and execute the SQL from 'sql/create_tables.sql'
    pass

#!user authentication functions
def register_user(username, password):
    """
    register a new user
    returns True if successful, False if username already exists
    """
    # TODO: Implement this function
    #* hash the password with bcrypt
    #* insert user into the database
    #* handle unique constraint violations
    pass

def verify_user(username, password):
    """
    Verify user credentials
    Returns user_id if valid, None if invalid
    """
    # TODO: Implement this function
    #* get user from database
    #* verify password hash with bcrypt
    pass

# history functions
def add_calculation_to_history(user_id, operation, expression, result):
    """
    add a calculation to user history
    keep only the last 5 calculations per user
    """
    # TODO: Implement this function
    #* insert new calculation
    #* delete older calculations if more than 5 exist
    pass

def get_user_history(user_id, limit=5):
    """
    get user's calculation history
    returns a list of the last 'limit' calculations
    """
    # TODO: Implement this function
    #* return the last 5 calculations for the user most recent first
    pass