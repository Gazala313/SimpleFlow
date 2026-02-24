from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer
from jose import jwt
import requests
import os

security = HTTPBearer()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")

JWKS_URL = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"

def get_current_user(token=Security(security)):
    jwks = requests.get(JWKS_URL).json()
    try:
        payload = jwt.decode(
            token.credentials,
            jwks,
            algorithms=["RS256"],
            audience=CLIENT_ID
        )
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
