import mysql.connector

# Database connection configuration
db_config = {
    'host': 'localhost',       # Replace with your DB host
    'user': 'your_username',   # Replace with your DB username
    'password': 'your_password', # Replace with your DB password
    'database': 'your_database'  # Replace with your DB name
}

# Establish the database connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)

# Query for all users
cursor.execute("SELECT username, password FROM users ORDER BY username ASC")
all_users = cursor.fetchall()

# Display all users
print("Users currently in the database:")
for user in all_users:
    print(f"Username: {user['username']}, Password: {user['password']}")

cursor.close()
conn.close()
