# src/app.py
import os
from flask import jsonify, redirect, url_for

# App factory & config
from src.create_app import create_app
from src.config import settings

# DB base (CHỈ dùng cho POC khi chưa có Alembic)
from src.infrastructure.databases import Base, engine


def init_db_if_needed():
    """
    Tạo schema tự động cho môi trường demo/POC khi:
    - INIT_DB=1 (mặc định 1)
    - Có URL kết nối MySQL hợp lệ
    Dùng Alembic trong môi trường thực tế.
    """
    init_db = os.getenv("INIT_DB", "1")
    if init_db == "1":
        try:
            Base.metadata.create_all(bind=engine)
            print("[INIT_DB] Created tables (POC mode). "
                  "For production, use Alembic migrations.")
        except Exception as ex:
            print(f"[INIT_DB] Failed to create tables: {ex}")


# Tạo app theo app-factory pattern
app = create_app()

# Route kiểm tra nhanh
@app.get("/")
def root():
    """
    Trang chào mừng mô phỏng IMS + link nhanh đến một số tài nguyên.
    """
    return jsonify({
        "app": "IMS – Intern Management System (demo)",
        "env": settings.ENV,
        "db": "MySQL via SQLAlchemy",
        "docs": {
            "users": "/api/users/",
            "interns": "/api/interns/",
            "recruitment": "/api/recruitments/",
            "applications": "/api/applications/",
            "trainings": "/api/trainings/",
            "projects": "/api/projects/",
            "assignments": "/api/assignments/",
            "evaluations": "/api/evaluations/"
        },
        "health": "/health"
    })


@app.get("/health")
def health():
    """
    Healthcheck đơn giản: trả 200 nếu app đang sống.
    (Có thể mở rộng: ping DB, cache, queue…)
    """
    return jsonify({"status": "ok"}), 200


def main():
    # Tạo bảng nếu bật POC mode
    init_db_if_needed()

    # Đọc HOST/PORT/DEBUG từ env (mặc định cho dev)
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "1") == "1"

    # Chạy app
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()
