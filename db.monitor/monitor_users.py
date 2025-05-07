import mysql.connector
import time

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_real_mysql_password',
    'database': 'calculator_db'
}


# Establish the database connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)

# Initialize the last seen user ID
last_seen_id = 0

print("Monitoring new users...\n")

try:
    while True:
        # Query for new users
        cursor.execute("SELECT * FROM users WHERE id > %s ORDER BY id ASC", (last_seen_id,))
        new_users = cursor.fetchall()
        
        # Display new users
        for user in new_users:
            print(f"New user added: {user}")
            last_seen_id = max(last_seen_id, user['id'])
        
        # Wait before the next check
        time.sleep(2)  # Check every 2 seconds

except KeyboardInterrupt:
    print("Monitoring stopped by user.")

finally:
    cursor.close()
    conn.close()
