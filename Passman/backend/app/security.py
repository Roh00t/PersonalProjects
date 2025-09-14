import os, secrets, base64
from datetime import datetime, timedelta
from typing import Optional
from itsdangerous import URLSafeTimedSerializer
from passlib.hash import argon2
from starlette.requests import Request
from starlette.responses import Response

SESSION_SECRET = os.getenv("SESSION_SECRET") or secrets.token_urlsafe(32)
COOKIE_NAME = os.getenv("COOKIE_NAME", "pm_session")
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "False").lower() == "true"
COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "Lax")

serializer = URLSafeTimedSerializer(SESSION_SECRET, salt="session")

def hash_password(pw: str) -> str:
    return argon2.using(rounds=3, memory_cost=102400, parallelism=8).hash(pw)

def verify_password(pw: str, pw_hash: str) -> bool:
    try:
        return argon2.verify(pw, pw_hash)
    except Exception:
        return False

def set_session(response: Response, data: dict, max_age: int = 3600):
    token = serializer.dumps(data)
    response.set_cookie(COOKIE_NAME, token, max_age=max_age, httponly=True, secure=COOKIE_SECURE, samesite=COOKIE_SAMESITE, path="/")

def get_session(request: Request, max_age: int = 3600) -> Optional[dict]:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    try:
        return serializer.loads(token, max_age=max_age)
    except Exception:
        return None

def clear_session(response: Response):
    response.delete_cookie(COOKIE_NAME, path="/")

def generate_csrf() -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(24)).decode()

def csp_headers(resp: Response):
    # Basic CSP; adjust for production
    resp.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "no-referrer"
    return resp
