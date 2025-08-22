import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    MYSQL_URL = os.getenv("MYSQL_URL")  # bắt buộc
    CORS_ORIGINS = [s.strip() for s in os.getenv("CORS_ORIGINS", "").split(",") if s.strip()]
    JSON_SORT_KEYS = False  # giữ nguyên thứ tự key

def require_mysql_url():
    if not Config.MYSQL_URL:
        raise RuntimeError("MYSQL_URL is not set in .env")
