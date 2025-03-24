import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()  # If using a .env file

def get_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        # Fallback to manual credentials or raise an error
        DATABASE_URL = "postgresql://postgres:mysecret@localhost:5432/trading_db"
    conn = psycopg2.connect(DATABASE_URL)
    return conn
