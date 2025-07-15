import flask
from flask import request, render_template, redirect, url_for, flash
from app.models.user_model import User
from auth.token_utils import generate_token, verify_token
from app.forms import (
    RegistrationForm,
    LoginForm,
    RequestResetForm,
    ResetPasswordForm,
    NewPasswordForm,
)
from app.routes.auth_routes_api import auth_bp
from werkzeug.security import generate_password_hash
from app.database import db
from flask_mail import Message
from app import mail
from .auth_routes_html import auth_bp
from app.logging_config import (
    log_login_attempt,
    log_password_reset_request,
    log_password_reset,
    log_event,
)


# Route to handle user registratiom for http form submission
@auth_bp.route("/register_form", methods=["GET", "POST"])
def register_form():

    form = RegistrationForm()

    if form.validate_on_submit():  # type: ignore

        username = form.username.data
        email = form.email.data
        password = form.password.data
        role = "user"

        # register the user
        if username and password and email:

            result = User.register_user(username, password, email, role)

            if result["success"]:

                flash("Registration successful!", "success")
                return redirect(url_for("auth.login_form"))

            else:
                flash(str(result["message"]), "warning")
                return render_template("register_html", form=form)

        else:
            flash("Please fill in all fields", "warning")

    return render_template("register_html", form=form)


# Route to handle user login for http form submission
@auth_bp.route("/login_form", methods=["GET", "POST"])
def login_form() -> flask.Response:

    form = LoginForm()

    if form.validate_on_submit():  # type: ignore
        # Get the username and password from the form
        username = form.username.data
        password = form.password.data

        if username is not None and password is not None:
            user = User.authenticate_user(username, password)

        else:
            user = None
            log_login_attempt(username or "", False)

        if user:
            flash("Login successful!", "success")
            log_login_attempt(username or "", True)

            return flask.make_response(redirect(url_for("main.index")))

        else:
            # If authentication fails, flash an error message
            flash("Invalid username or password", "danger")
            return flask.make_response(render_template("login_html", form=form))

    return flask.make_response(render_template("login_html", form=form))


# Route to handle password reset request and send emails  generates token, and sends a reset
# link to the user's email containing the token"""
@auth_bp.route("/reset_password_form", methods=["GET", "POST"])
def reset_password_request() -> flask.Response:

    form = RequestResetForm()

    if form.validate_on_submit():  # type: ignore

        email = form.email.data

        if not email:
            # If email is not provided, flash a warning message
            flash("Please enter your email address", "warning")
            return flask.make_response(render_template("reset_password_request.html"))

        # Check if the user exists with the provided email
        user = User.get_user_by_email(email)

        if user:
            # Generate a token for the user
            token = generate_token({"username": user.username})
            User.update_token(user.username, token)

            # Generate the reset link
            reset_link = url_for(
                "auth.reset_password_form", token=token, _external=True
            )

            # Send the reset link to the user's email
            msg = Message(
                subject="Password Reset Request",
                recipients=[email],
                body=f"Click the link to reset your password: {reset_link}",
            )
            try:

                mail.send(msg)

            except Exception as e:

                flash(f"An error occurred while sending the email: {str(e)}")
                return flask.make_response(
                    flask.redirect(url_for("auth_bp.reset_password_request"))
                )

            flash(f"Password reset link has been sent to {email}", "info")
            return flask.make_response(flask.redirect(url_for("auth.login_form")))

        else:
            flash("No user found with that email adress", "warning")
            return flask.make_response(
                flask.redirect(url_for("auth_bp.reset_password_request"))
            )

    return flask.make_response(render_template("reset_password_request.html"))


# Route to handle password reset using the token sent via email
# This route verifies the token and allows the user to set a new password
@auth_bp.route("/reset_password_form/<token>", methods=["GET", "POST"])
def reset_password(token: str) -> flask.Response:
    data = verify_token(token)

    if not data:
        # If the token is invalid or expired, flash an error message and redirect
        flash("The reset link is invalid or has expired. Make a new request", "danger")
        return flask.make_response(
            flask.redirect(url_for("auth.reset_password_request"))
        )

    form = ResetPasswordForm()

    if form.validate_on_submit():  # type: ignore

        new_password = request.form.get("new_password")
        user = User.get_user_by_username(data["username"])

        # Check if the user exists, update the password
        if user:

            if new_password is None:

                flash("Please provide a new password", "warning")
                return flask.make_response(
                    flask.redirect(url_for("auth.reset_password_form", token=token))
                )
            user.hashed_password = generate_password_hash(new_password)

            db.session.commit()

            log_password_reset(user.username, True)

            flash("Your password has been reset successfuly", "success")
            return flask.make_response(flask.redirect(url_for("auth.login_form")))

        else:
            flash("User not found", "warning")

            # Log the password reset request with an empty username
            log_password_reset_request(username="", email=data["email"])

            return flask.make_response(
                flask.redirect(url_for("auth.reset_password_request"))
            )

    # Render the reset password form if GET request
    return flask.make_response(render_template("reset_password.html", token=token))
