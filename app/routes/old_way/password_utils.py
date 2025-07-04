import hashlib
import os

#Not needed for the code to work as we have werkzeug security module imported
#but for demonstation purposes we can use this code to hash passwords
#password expected to be string as well as hashed password which is a function return value
def hash_password(password:str) -> str: 
    
    #generates 16 bytes random sequence - salt
    salt = os.urandom(16) 
    
    # converts password string to bytes combining them together into one object firs
    salted_password = salt + password.encode('utf-8') 

    #Hashes the salted_password using SHA-256 and returns it as hexadecimnal string
    hashed_password = hashlib.sha256(salted_password).hexdigest()

    #returns the salt for later verification and the hashed and salted password
    return f"{salt.hex()}${hashed_password}"


def verify_password(password:str, hashed_password:str) -> bool:
    try:
        #split hashed_password into salt_hex and stored_hash
        salt_hex, stored_hash = hashed_password.split('$')
        #convert salt from hex to bytes
        salt = bytes.fromhex(salt_hex)
        test_hash = hashlib.sha256(salt + password.encode('utf-8')).hexdigest()
        return test_hash == stored_hash
    
    except Exception:
        return False










