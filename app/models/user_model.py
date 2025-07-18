"""
User model and user management methods for Flask authentication system.
This module defines the User database model and provides class methods for user registration,
authentication, credential updates, token management, and deletion.
"""

from __future__ import annotations
from datetime import datetime
from app.database import db
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from auth.token_utils import generate_token


class User(db.Model):
    """
    SQLAlchemy model representing a user.    
    """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(
        self, username: str, email: str, hashed_password: str, token: str, role: str
    ):
        """
        Initialize a new User instance.
        """
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.token = token
        self.role = role
    
    @classmethod
    def get_user_by_username(cls, username: str) -> Optional["User"]:
        """Retrieve a user by username"""
        return cls.query.filter_by(username=username).first()  # type: ignore
    
    
    @classmethod
    def get_user_by_email(cls, email: str) -> Optional["User"]:
        """Retrieve a user by email"""
        return cls.query.filter_by(email=email).first()  # type: ignore

    
    @classmethod
    def register_user(        
        cls, username: str, password: str, email: str, role:str
    ) -> dict[str, bool | str]:
        
        """Register a new user if the username and email are unique
        Returns: dict[str, bool | str]: Dictionary with registration result and message."""
        
        from app import db        
        # Check for existing username or email
        if cls.get_user_by_username(username):
            return {"success": False, "message": "Username already exists"}
        if cls.get_user_by_email(email):
            return {"success": False, "message": "Email already exists"}

        # Generate token and hash password
        token = generate_token({"username": username, "role": "user"})
        user = cls(
            username=username,
            email=email,
            hashed_password=generate_password_hash(password),
            token=token,
            role="user",
        )
        

        # Add user to DB
        db.session.add(user)
        db.session.commit()
        return {
            "success": True,
            "message": "User registered successfully",
            "token" : token,
        }

    
    @classmethod
    def authenticate_user(cls, username: str, password: str) -> Optional["User"]:
        """Authenticate a user by username and password.
        Returns: Optional[User]: User instance if credentials are correct, else None."""
        user = cls.get_user_by_username(username)
        if user and check_password_hash(user.hashed_password, password):
            return user
        return None

    
    @classmethod
    def user_authenticated(cls, username: str, password: str) -> bool:
        """Check if user credentials are valid.        
        Returns: bool: True if authentication succeeds, else False."""
        user = cls.authenticate_user(username, password)
        return user is not None

    
    @classmethod
    def delete_user(cls, username: str) -> Optional["User"]:        
        """ Delete a user by username.
        Returns: Optional[User]: The deleted User instance if found, else None."""
        user = cls.get_user_by_username(username)
        if user:
            db.session.delete(user)
            db.session.commit()
            return user
        return None

    
    @classmethod
    def update_user(
        cls,
        username: str,
        new_username: str,
        password: str,
        new_password: str,
        email: str,
        new_email: str,
        role: str,
        new_role: str,
    ) -> Optional["User"]:
        """
        Update a user's credentials. Only non-empty new values are applied.
        Returns: Optional[User]: The updated User instance if found, else None.
        """
        user = cls.get_user_by_username(username)
        if user:
            if new_username:
                user.username = new_username
            if new_password:
                user.hashed_password = generate_password_hash(new_password)
            if new_email:
                user.email = new_email
            if new_role:
                user.role = new_role
            db.session.commit()
            return user
        return None

    @classmethod
    def update_token(cls, username: str, token: str) -> Optional["User"]:
        """
        Update the user's token.        
        Returns:Optional[User]: The updated User instance if found, else None.
        """
        user = cls.get_user_by_username(username)
        if user:
            user.token = token
            db.session.commit()
            return user
        return None

    def __repr__(self):
        """
        Return a string representation of the user.
        """
        return f"<User {self.username} {self.role}>"
