from hashlib import sha256
import os
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer as Serializer, BadSignature, SignatureExpired
from typing import Any, Dict, cast



load_dotenv()



_secret_key = os.environ.get("SECRET_KEY")
if _secret_key is None:
    raise ValueError("Secret key not found in environment variables")
SECRET_KEY:str



def generate_token(data: dict[str,str], expires_sec: int = 3600) -> str:
    s = Serializer(SECRET_KEY)
    token =  s.dumps(data)
    # Ensure token is always a string
    if isinstance (token, bytes):
        token = token.decode('utf-8')
    return token



def verify_token(token:str, expires_sec: int = 3600) -> dict[str, Any] | None:
    """Verify a token and return data if valid else raise an error"""
    s = Serializer(SECRET_KEY)
    
    try:

        data = cast(Dict[str, Any],s.loads(token, max_age=expires_sec))
        return data
    
    except SignatureExpired:
        return None #token has epired
    
    except BadSignature:
        return None #Invalid token
    


def validate_token(token:str) -> bool:
    return verify_token(token) is not None #is note None if valid else None



def hash_token(token: str) -> str:
    """Hash a token using SHA-256."""
    hash_object =  sha256(token.encode('utf-8'))
    hex_digest = hash_object.hexdigest()
    return hex_digest





