from werkzeug.security import check_password_hash
from app.models import User
from app.database import db
from auth.token_utils import generate_token
from typing import cast




def login_user(username: str, password: str) -> dict[str, str | bool]:
    
    user = cast( User | None , User.query.filter_by(username=username).first())

    if not user:
        return {"success":False, "message": "User not found"}
    assert user is not None
      
    if not check_password_hash(user.hashed_password, password):
        return {"success":False, "message": "Incorect password"}

    
    #generate a new token
    token=generate_token({"username":user.username, "role": user.role})
    token = token
    
    
    try:
        db.session.commit()
    except Exception as e:
        return {"success": False, "message": f"Database error: {str(e)}"}

    
    return {

        "success":True, 
        "message": "Login successful",
        "token": token,
        "username": username,
        "role": user.role

    }


