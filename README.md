your_project/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── auth/
│   │   ├── __init__.py               # hash_password, check_password
│   │   ├── register_user.py
│   │   ├── login_user.py
│   │   ├── token_utils.py
│   │   ├── password_reset.py         # (Planned)
│   │   ├── email_utils.py            # (Planned)
│   │
│   ├── decorators/
│   │   └── secure_access.py          # Token check + 30s protection
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   └── main.py
│   │
│   ├── models/
│   │   └── __init__.py 
        └── user_model.py 
            
│   │
│   ├── templates/                    # Optional
│   └── static/                       # Optional
│
├── access_log.txt                    # Logs validated access attempts
├── create_db.py                      # Initializes users.db
├── requirements.txt
├── .env
├── README.md
├── run.py



Code Execution Flow

    You run python run.py → imports and calls create_app() from app/__init__.py

    In app/__init__.py:

        Loads config via Config class in config.py

        Initializes logging and database connection

        Registers blueprints like auth_bp (from routes/auth_routes.py)

    On a request to /register:

        Routed via auth_bp in auth_routes.py

        Calls register_user() in register.py

        Uses hash_password() from auth/__init__.py

        Writes to the database

        Optionally logs via logging_utils.py

    On a request to /login:

        Routed through auth_bp

        Calls login_user() in login.py

        Validates password

        Generates token and logs access

    Secure endpoints:

        Decorated with @token_required or @secure_access

        Decorator pulls token from request headers, checks time window, validates

    All actions (register/login/secure API call) can be logged in access_log.txt.

