from app import create_app
from app.models.user_model import User

app = create_app()

with app.app_context():
    
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    role = input("Enter role: ")

    user = User.register_user(username, password, email, role)
    
    if user:
        print(f"User {user['username']} registered successfully.")
    else:
        print("Registration failed. Please check your details.")