import logging
from logging.config import dictConfig

def init_logging(app=None):
    """Cấu hình logging cơ bản cho ứng dụng Flask"""

    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default"
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["wsgi"]
        }
    })

    if app:
        app.logger.info("Logging đã được khởi tạo.")
