import os

BACKEND_URL = "http://localhost:8000" if not os.environ.get("BACKEND_URL") else os.environ.get("BACKEND_URL")
FRONTEND_URL = "http://localhost:5173/#/login-success" if not os.environ.get("FRONTEND_URL") else os.environ.get("FRONTEND_URL")
USERMANAGER_URL = "http://localhost:3000" if not os.environ.get("USERMANAGER_URL") else os.environ.get("USERMANAGER_URL")

TOKEN_REDIRECT_URL = f"{USERMANAGER_URL}/auth/login-form?r={BACKEND_URL}/auth/token"
