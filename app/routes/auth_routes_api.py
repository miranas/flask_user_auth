from flask import Blueprint, request, jsonify, url_for
from typing import Any
from app.models.user_model import User
from auth.token_utils import generate_token, verify_token
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user #type: ignore
from app.database import db
from flask_mail import Message
from app import mail
from app.logging_config import log_login_attempt, log_password_reset_request, log_password_reset, log_event



# Blueprint for authentication routes 
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")



#Route to handle user registration for API endpoint, React frontend
@auth_bp.route('/register', methods = ['POST'])
def register():

    data: dict[str,Any] = request.get_json() or {}
    username: str | None = data.get('username')
    password: str | None = data.get('password')
    email: str | None = data.get('email') #type: ignore

    #Always set role to user for self registration
    role: str = "user"
   
    if not username or not password:
        return jsonify({"success":False,"message":"Missing username or password"}),400
        #login attempts failed
        log_login_attempt(username, False)

    result = User.register_user(username, password, role)

    # login attemts successful
    log_login_attempt(username, True)
    
    return jsonify(result), 201 if result ["success"] else 404




## Route to handle user login for API endpoint, React frontend
@auth_bp.route('/login', methods=['POST'])
def login():

    data: dict[str, Any] = request.get_json() or{}
    username: str | None = data.get('username')
    password: str | None = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Missing username or password"}), 400
    
    user = User.get_user_by_username(username)
    if not user or not User.authenticate_user(user.username, password):
        return jsonify({"success": False, "message": "Invalid username or password"}), 401
    
    # Generate token for the user
    token = generate_token({"username": user.username, "role": user.role})  
    
    user.token = token

    db.session.commit()

    return jsonify({

        "success": True,
        "message": "Login successful",
        "token":token,
        "username": user.username,
        "role": user.role

    }), 200





@auth_bp.route('reset_password_request', methods = ['POST', 'GET'])
def reset_password_request():

    data: dict[str, Any] = request.get_json () or {}
    email = data.get('email')

    if not email:
        return jsonify({"success":False, "message":"Email is required"}),400
    
    user = User.get_user_by_email(email)
    if not user:
        return jsonify({"success":False, "message":"User not found"}),404
    
    # Generate a token for the user
    token = generate_token({"username":user.username, "role":user.role})

    # Update the user's token in the database
    user.token = token

    db.session.commit()

    reset_link: str = url_for("auth.reset_password", token = token, external = True)

    # Send the reset link to the user's email

    msg = Message(

        subject = "Password reset request",
        recipients = [email],
        body = f"Click the link to reset your password: {reset_link}"
    
    )

    try:
        mail.send(msg)

    except Exception:
        return jsonify ({"success":False, "message": F"Failed to send email."}),500
    
    return jsonify ({"success":True, "message": "Password reset link sent to your email {email}"}),200




# Route to handle password reset using the token sent via email
# This route verifies the token and allows the user to set a new password      
@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token: str):

    data: dict[str, Any] | None = verify_token(token)
    if not data:
        return jsonify({"success": False, "message": 'The reset link is invalid or has expired. Make new request'}), 400

    req_data: dict[str, Any] = request.get_json() or {}
    new_password: str | None = req_data.get('new_password')

    if not new_password:
        return jsonify({"success": False, "message": "New password is required"}), 400

    # Get the user by username from the token data
    user = User.get_user_by_username(data['username'])

    if user:

        user.hashed_password = generate_password_hash(new_password)
        db.session.commit()
        log_password_reset(user.username, True)
        return jsonify({"success": True, "message": "Password reset successful"}), 200
    
    else:
        
        log_password_reset_request(username = "", email=data['email'])
        return jsonify({"success":False, "message": "User not found"}),404




"""API endpoint to get the current user's profile info used by React or any other frontend that consumes REST API"""
@auth_bp.route('/profile', methods = ['GET'])
@login_required
def profile_api():
    

    if not current_user.is_authenticated:
        return jsonify({"success": False, "message": "User not authenticated"}), 401
    
    
    user = current_user

    return jsonify(
        {
            "success": True,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.strftime("%d-%m-%Y %H:%M:%S")
            
        }


    )








                        
    
    







