import logging
from datetime import datetime

logging.basicConfig(
    filename= 'access.log',
    level = logging.INFO,
    format = '%(asctime)s: %(levelname)s %(message)s'
    
)

def log_event(event_type:str, username:str = "", status:str="", message:str = ""):
    log_msg = f"{event_type} | user: {username} | Status: {status}, Message: {message}"
    logging.info(log_msg)

def log_login_attempt(username:str, success:bool):
    status = "SUCCESS" if success else "FAILURE"
    log_event("LOGIN_ATTEMPT", username, status)


def log_password_reset_request(username:str, email:str):
    log_event("PASSWORD RESET REQUEST", username=username, message=f"Password reset requested for {email}")

def log_password_reset(username:str, success:bool):
    status = "SUCCESS" if success else "FAILURE"
    log_event("PASSWORD_RESET", username=username, status=status)   
    



