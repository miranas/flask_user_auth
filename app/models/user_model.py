from datetime import datetime
from ..database import db
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from auth.token_utils import generate_token




class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique=True, nullable = False)
    username = db.Column(db.String(80), unique= True, nullable=False)
    hashed_password = db.Column(db.String(200), nullable = False)
    token = db.Column(db.String(200), nullable = False)
    role = db.Column(db.String(50), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    
    
    def __init__(
        self,
        username: str,
        email: str,
        hashed_password: str,
        token: str,
        role: str
    ):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.token = token
        self.role = role

           
    
    @classmethod
    def get_user_by_username(cls, username: str) -> Optional['User']:
        """Retrieve a user by username"""
        return cls.query.filter_by(username=username).first() 
    

    
    @classmethod
    def get_user_by_email(cls, email:str) -> Optional['User']:
        """retrieve a user by email"""
        return cls.query.filter_by(email=email).first()
    

    # User registration method
    @classmethod    
    def register_user(cls, username:str, password:str, email:str) -> dict[str, bool | str]:
        
        
        from app import db

        if cls.get_user_by_username(username):
            return {"success": False, "message": "Username already exists"}
        
        if cls.get_user_by_email(email):
            return {"success": False, "message": "Email already exists"}
        
        
        token = generate_token({"username":username, "role": "user"})
        
        
        user = cls(

            username=username,
            email=email,
            hashed_password=generate_password_hash(password),#password is hashed here
            token=token,
            role="user"
        )   

        # Add the user to the database
        db.session.add(user)
        db.session.commit()

        return {"success":True, "message": "User registered successfuly"}
    
    

    
    @classmethod
    def authenticate_user(cls, username:str, password:str) -> Optional['User']:
        """Authenticate a user by username and password"""
        
        user = cls.get_user_by_username(username)

        if user and check_password_hash(user.hashed_password, password):
            return user
        
        return None  
    
    
    
    @classmethod
    def user_authenticated(cls, username:str, password:str) -> bool:
        """Check if user credentials are valid"""
        user = cls.authenticate_user(username, password)
        return user is not None
    


    @classmethod 
    def delete_user(cls, username:str) -> Optional['User']:
        """Delete a user by username"""
        
        user = cls.get_user_by_username(username)

        if user:
            db.session.delete(user)            
            db.session.commit()
            return user
        
        return None
    

    
    @classmethod
    def update_user(cls, username:str,new_username:str, password:str, new_password:str, email:str,new_email:str, role:str, new_role:str) -> Optional['User']:
        """Update a user's credentials"""
        user = cls.get_user_by_username(username)

        if user:
            user.username = new_username if new_username else user.username
            user.hashed_password = generate_password_hash(new_password) if new_password else user.hashed_password
            user.email = new_email if new_email else user.email
            user.role = new_role if new_role else user.role
            db.session.commit()
            return user
        
        return None
    

    @classmethod
    def update_token(cls, username:str, token:str) -> Optional['User']:
        """Update the user's token"""
        user = cls.get_user_by_username(username)
        if user:
            user.token = token
            db.session.commit()
            return user
        
        return None
             
    

  
    
    def __repr__(self):
        return f"<User {self.username} {self.role}>"
    



