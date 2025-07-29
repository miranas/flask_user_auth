from flask_wtf import FlaskForm # type: ignore
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Pasword',validators=[DataRequired()])
    submit = SubmitField('Login')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators = [DataRequired(), Length (min=8)])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Rset Password')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Requset Password Reset')

