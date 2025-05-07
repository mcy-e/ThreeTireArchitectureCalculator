import psycopg2
from config import Config

try:
    conn = psycopg2.connect(
        host=Config.DB_HOST,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        port=Config.DB_PORT
    )
    print("✅ Successfully connected to the database!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")