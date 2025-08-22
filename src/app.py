# src/app.py
import os
from flask import Flask
from dotenv import load_dotenv

# Logging & Error handler
from app_logging import init_logging
from error_handler import register_error_handlers

# Controllers (Blueprints)
from src.api.controllers.user_controller import users_bp
from src.api.controllers.intern_controller import interns_bp
from src.api.controllers.recruitment_controller import bp as recruitment_bp
from src.api.controllers.application_controller import bp as application_bp
from src.api.controllers.training_controller import training_bp
from src.api.controllers.project_controller import project_bp
from src.api.controllers.assignment_controller import assignment_bp
from src.api.controllers.evaluation_controller import evaluations_bp


def create_app():
    load_dotenv()  # đọc biến môi trường từ .env
    app = Flask(__name__)

    # 1. Logging
    init_logging(app)

    # 2. Error handler chung
    register_error_handlers(app)

    # 3. Đăng ký các Blueprint
    app.register_blueprint(users_bp,        url_prefix="/api/users")
    app.register_blueprint(interns_bp,      url_prefix="/api/interns")
    app.register_blueprint(recruitment_bp)   # đã có prefix trong controller
    app.register_blueprint(application_bp)   # đã có prefix trong controller
    app.register_blueprint(training_bp)      # đã có prefix trong controller
    app.register_blueprint(project_bp)       # có thể đã prefix "/api/projects"
    app.register_blueprint(assignment_bp)    # đã có prefix trong controller
    app.register_blueprint(evaluations_bp, url_prefix="/api/evaluations")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
