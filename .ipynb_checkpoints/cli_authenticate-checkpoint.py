from app import create_app
from app.models.user_model import User

app = create_app()

with app.app_context():
    
    username = input("Enter username: ")
    password = input("Enter password: ")

    user = User.authenticate_user(username, password)

    if user:
        print(f"User {user.username} authenticated successfully.")
    else:
        print("Authentication failed. Please check your credentials.")
        
