import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    JWT_SECRET = os.environ.get("JWT_SECRET")
    FRONTEND_URL = os.environ.get("FRONTEND_URL")
    DATABASE_URL = os.environ.get("DATABASE_URL")