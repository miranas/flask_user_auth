from flask import Blueprint, request, jsonify
from typing import Any
from app.models.user_model import User
from flask import request, render_template, url_for, flash , redirect
from auth.token_utils import generate_token, verify_token
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user #type: ignore


# Blueprint for authentication routes
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")



#Route to handle user registration  for API endpoint, React frontend
@auth_bp.route('/register', methods = ['POST'])
def register():

    data: dict[str,Any] = request.get_json() or {}
    username: str | None = data.get('username')
    password: str | None = data.get('password')

    #Always set role to user for self registration
    role: str = "user"

   
    if not username or not password:
        return jsonify({"success":False,"message":"Missing username or password"}),400
    
    result = User.register_user(username, password, role)
    
    return jsonify(result), 201 if result ["success"] else 404





    


        



@auth_bp.route('/reset-password/<token>', methods=['GET','POST'])
def reset_password(token:str):
    data = verify_token(token)

    if not data:
        flash('The reset link is invalid or has expired. Make new request','danger')
        return redirect(url_for('reset_password_request'))

    if request.method == "POST":
        new_password = request.form('new_password')
        user = User.get_user(data['username'])

        if user:
            user.hashed_password = generate_password_hash(new_password)
            db.session.commit()
            flash("Your password has been reset successfully", 'success')
            return_redirect(url_for(auth.login))
        else:
            flash ('User not found', 'warning')
            return redirect(url_for('auth.reset_password_request'))
    return render_template('reset_pasword.html', token=token)





"""API endpoint to get the current user's profile info
    Used by React or any other frontend that consumes REST API"""

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








                        
    
    







