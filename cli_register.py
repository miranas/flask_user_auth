from app import create_app
from app.models.user_model import User

app = create_app()

with app.app_context():
    
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    user = User.register_user(username, password, email)

    print(f"User {user.username} registered successfully.")
