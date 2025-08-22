# src/config.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()  # Đọc .env ở root


@dataclass(frozen=True)
class Settings:
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "1") == "1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")

    # DB
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "MYSQL_URL",
        "mysql+pymysql://root:1234@127.0.0.1:3306/ims?charset=utf8mb4"
    )

    # CORS
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")  # CSV hoặc *

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # POC init DB (create_all) — nên OFF khi dùng Alembic
    INIT_DB: bool = os.getenv("INIT_DB", "1") == "1"


settings = Settings()
