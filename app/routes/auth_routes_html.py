import flask
from flask import request, render_template, redirect, url_for, flash, Response
from app.models.user_model import User
from auth.token_utils import generate_token, verify_token
from app.forms import RegistrationForm
from flask_login import login_required, current_user #type: ignore
from app.routes.auth_routes_api import auth_bp
from werkzeug.security import generate_password_hash
from app.database import db
from app.forms import LoginForm, RegistrationForm




#Route to handle user registratiom for http form submission
@auth_bp.route('/register_form', methods=['GET','POST'])
def register_form():
    
    form = RegistrationForm()

    if form.validate_on_submit():  # type: ignore
        
        username = form.username.data
        email = form.email.data
        password = form.password.data

        #register the user
        if username and password and email:

            result = User.register_user(username, password, email)
            
            if result["success"]:
                    
                    flash('Registration successful !', 'success')
                    return redirect(url_for('auth.login_form'))
            
            else:
                flash(str(result["message"]), 'warning')
                return render_template('register_html', form=form)
        
        else:
            flash ('Please fill in all fields','warning')
    
    
    return render_template('register_html', form=form)




#Route to handle user login for http form submission
@auth_bp.route('/login_form', methods=['GET', 'POST'])
def login_form() -> flask.Response:
    
    form = LoginForm()

    if form.validate_on_submit():  # type: ignore
        username = form.username.data
        password = form.password.data

        if username is not None and password is not None:
            user = User.authenticate_user(username, password)
        else:
            user = None

        if user:
            flash('Login successful!', 'success')
            return flask.make_response(redirect(url_for('main.index')))
        else:
            flash('Invalid username or password', 'danger')
            return flask.make_response(render_template('login_html', form=form))
   
    return flask.make_response(render_template('login_html', form=form))




#Route to handle password reset request and send emails  generates token, and sends a reset
#link to the user's email containing the token
@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request() -> flask.Response:
    if request.method == 'POST':
        email = request.form.get('email')

        if not email:
            flash('Please enter your email address', 'warning')
            return flask.make_response(render_template('reset_password_request.html'))

        user = User.get_user_by_email(email)

        if user:
            # Generate a token for the user
            token = generate_token({'username': user.username})
            User.update_token(user.username, token)

            # Generate the reset link 
            reset_link = url_for('auth_bp.reset_password', token=token, _external=True)

            flash(f'Password reset link has been sent to {email}', 'info')
            return flask.make_response(flask.redirect(url_for('auth.login_form')))

        else:
            flash('No user found with that email adress', 'warning')
            return flask.make_response(flask.redirect(url_for('auth_bp.reset_password_request')))

    return flask.make_response(render_template('reset_password_request.html'))




@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token: str) -> flask.Response:
    data = verify_token(token)

    if not data:
        flash('The reset link is invalid or has expired. Make a new request', 'danger')
        return flask.make_response(flask.redirect(url_for('auth.reset_password_request')))

    if request.method == "POST":
        new_password = request.form.get('new_password')
        user = User.get_user_by_username(data['username'])

        if user:
            if new_password is None:
                flash('Please provide a new password', 'warning')
                return flask.make_response(flask.redirect(url_for('auth.reset_password', token=token)))
            user.hashed_password = generate_password_hash(new_password)
            
            db.session.commit()

            flash("Your password has been reset successfuly", 'success')
            return flask.make_response(flask.redirect(url_for('auth.login_form')))
        
        else:
            flash ('User not found', 'warning')
            return flask.make_response(flask.redirect(url_for('auth.reset_password_request')))
    
    # Render the reset password form if GET request
    return flask.make_response(render_template('reset_password.html', token=token))






                


                        
        

        