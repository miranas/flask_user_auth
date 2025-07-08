from app.models.user_model import User
from app import create_app


def test_register_user():
    app = create_app()
    with app.app_context():
        user = User.get_user_by_username("testuser")
        if user:
            from app.database import db
            db.session.delete(user)
            db.session.commit()

        response = User.register_user("testuser", "password12345", "user")
        assert response["success"] is True
        
        print (response)

def test_pytest_discovery():
    assert True


def test_authenticate_user():

    app = create_app()
    with app.app_context():
        user = User.get_user_by_username("testuser")
        if not user:
            print("User not found")

        authenticated_user = User.authenticate_user("testuser", "password12345")
        assert authenticated_user is not None
        assert authenticated_user.username == "testuser"
        
        print (authenticated_user)
