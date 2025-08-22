# src/cors.py
from flask import Flask
from flask_cors import CORS
from src.config import settings


def init_cors(app: Flask) -> None:
    """
    Bật CORS cho ứng dụng.
    - settings.CORS_ORIGINS có thể là '*' hoặc danh sách CSV ('http://localhost:3000,http://localhost:5173')
    """
    origins_cfg = settings.CORS_ORIGINS
    if origins_cfg.strip() == "*":
        origins = "*"
    else:
        origins = [o.strip() for o in origins_cfg.split(",") if o.strip()]

    CORS(
        app,
        resources={r"/api/*": {"origins": origins}},
        supports_credentials=True,
        expose_headers=["X-Request-ID"],
    )
