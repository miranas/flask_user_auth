import time
from typing import Any, Callable


def secure_access(
        
        expected_username: str,
        expected_role: str,
        expected_token: str, 
        allowed_window_start: float = time.time()
    ):

    def decorator(func:Callable[..., Any]) -> Callable[...,Any]:
        
        def wrapper(*args:Any, **kwargs:Any)-> Any:
            
            """Decorator to secure access to a function based on username, role, and token."""
            current_time = time.time()
            username = kwargs.get('username')
            token = kwargs.get('token')
            role = kwargs.get('role')
            status = kwargs.get('status')
            access_time = time.strftime("%D-%M-%Y @ %H:%M:%S")

            
            #time window check
            if current_time - allowed_window_start > 30:
                status = "Access Denied (Time Window Expired)"
                access_time = time.strftime("%D-%M-%Y @ %H:%M:%S")
                print("Access denied: Login attempt outside the allowed 30-second window.")
            
            elif username != expected_username or token != expected_token or expected_role != role:
                status = "Access Denied"
                print(f"DENIED attempt to access  by user: {username}, please provide the correct credentials")

            else:
                status = "Access Granted"
                print("Access granted!")


            log_entry: dict[str,str | None]= {
                    
                    "timestamp": access_time,
                    "username": kwargs.get('username'),
                    "role": kwargs.get('role'),
                    "function": func.__name__,
                    "status": status
                }   

            print(f"Access attempt by user: {kwargs.get('username')}, with role: {kwargs.get('role')} at {access_time} resulted in: {status}")
            
            with open("access_log.txt", "a") as log_file:
                log_file.write(f"{log_entry}\n")
                return None    

            
                           
            return func(*args, **kwargs)
            
        return wrapper
    
    return decorator


@secure_access("admin", "admin", "1234")
def sensitive_operation(*args, **kwargs):
    print("Accessing sensitive data...")

# User input for testing
username = input("Enter username: ")
role = input("Enter role: ")


sensitive_operation(username=username, role=role, token=token)