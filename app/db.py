import psycopg2
from psycopg2 import sql, OperationalError
from datetime import date
from typing import Optional
from app.config import DATABASE_URL

# Global sync connection
DB_CONN = None

def init_db_connection(dsn: str = DATABASE_URL) -> None:
    """
    Initializes the global database connection with appropriate isolation level.
    """
    global DB_CONN
    try:
        DB_CONN = psycopg2.connect(dsn)
        #DB_CONN.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
        print("Database connection initialized.")
    except OperationalError as e:
        print(f"Error initializing DB connection: {e}")
        raise

def get_user_birthdate(username: str) -> Optional[date]:
    """
    Fetches the birthdate of a user by username.
    """
    try:
        with DB_CONN.cursor() as cursor:
            cursor.execute(
                "SELECT date_of_birth FROM users WHERE username = %s",
                (username,)
            )
            row = cursor.fetchone()
            return row[0] if row else None
    except Exception as e:
        print(f"Error fetching user: {e}")
        raise

def upsert_user(username: str, day_birthday: date) -> None:
    """
    Inserts or updates a user's date of birth in the database.
    """
    try:
        with DB_CONN.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (username, date_of_birth)
                VALUES (%s, %s)
                ON CONFLICT (username)
                DO UPDATE SET date_of_birth = EXCLUDED.date_of_birth
                """,
                (username, day_birthday)
            )
        DB_CONN.commit()
    except Exception as e:
        DB_CONN.rollback()
        print(f"Error during upsert: {e}")
        raise
