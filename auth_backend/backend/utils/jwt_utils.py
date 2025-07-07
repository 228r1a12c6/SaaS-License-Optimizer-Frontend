# auth_backend/backend/utils/jwt_utils.py

import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"  # In production, use a secure, environment-based value.

def generate_token(email):
    """
    Generate a JWT token for the given user email.
    """
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=1)  # 1-hour expiry
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    """
    Decode the JWT token and return the payload if valid.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
