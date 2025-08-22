# src/create_app.py
from flask import Flask, request

from src.config import settings
from src.app_logging import init_logging, ensure_request_id
from src.cors import init_cors
from src.error_handler import register_error_handlers

# (POC) create_all: chỉ dùng trong dev/demo. Production dùng Alembic.
from src.infrastructure.databases import Base, engine

# Controllers (Flask Blueprints)
from src.api.controllers import (
    user_controller,
    intern_controller,
    recruitment_controller,
    application_controller,
    training_controller,
    project_controller,
    assignment_controller,
    evaluation_controller,
)


def _maybe_init_db():
    """Tạo bảng tự động khi chạy POC/dev (settings.INIT_DB=True)."""
    if settings.INIT_DB:
        try:
            Base.metadata.create_all(bind=engine)
            print("[INIT_DB] Created tables (POC/dev). Use Alembic in production.")
        except Exception as ex:
            print(f"[INIT_DB] Failed to create tables: {ex}")


def create_app() -> Flask:
    """App factory: cấu hình Flask app theo Layered Architecture của IMS."""
    # 1) Logging
    init_logging(settings.LOG_LEVEL)

    # 2) Tạo app + config cơ bản
    app = Flask(__name__)
    app.config["ENV"] = settings.ENV
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    # 3) Middleware gắn request-id sớm
    @app.before_request
    def _attach_request_id():
        ensure_request_id(request.environ)

    # 4) CORS & Error handlers
    init_cors(app)
    register_error_handlers(app)

    # 5) Đăng ký Blueprints (REST API)
    app.register_blueprint(user_controller.bp, url_prefix="/api/users")
    app.register_blueprint(intern_controller.bp, url_prefix="/api/interns")
    app.register_blueprint(recruitment_controller.bp, url_prefix="/api/recruitments")
    app.register_blueprint(application_controller.bp, url_prefix="/api/applications")
    app.register_blueprint(training_controller.bp, url_prefix="/api/trainings")
    app.register_blueprint(project_controller.bp, url_prefix="/api/projects")
    app.register_blueprint(assignment_controller.bp, url_prefix="/api/assignments")
    app.register_blueprint(evaluation_controller.bp, url_prefix="/api/evaluations")

    # 6) (Dev/POC) Tạo bảng lần đầu nếu cần
    _maybe_init_db()

    return app
