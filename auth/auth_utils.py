import sqlite3
from .password_utils import verify_password
from typing import Optional


DB_PATH = 'users.db'


def get_user(username: str):
    """Retrieve a user from the database by username."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def validate_user(username: str, password: Optional[str] = None, token: Optional[str] = None):
    """Validate a user by username and either password or token."""
    user = get_user(username)
    if not user:
        return None
    if password:
        return verify_password(password,user["hashed_password"])
    if token:
        return token == user["token"]

        
    return False 
    