from werkzeug.security import generate_password_hash
from app import db
from app.models.user_model import User
from ...auth.token_utils import generate_token
from typing import cast



def register_user(username:str, password:str, role:str) -> dict[str,str | bool]:

    existing_user = cast(User | None, User.query.filter_by(username=username).first())

    if existing_user:
        return{"success": False,"message": "Username already exists"}
    
    
    password_hash = generate_password_hash(password)
    
    token = generate_token({"username": username, "role":role})

    new_user = User(username=username, hashed_password=password_hash, token=token, role=role)

    db.session.add(new_user)
    
    db.session.commit()

    return{ 

        "success": True,
        "message": "User registered successfully!"
    }

                    



