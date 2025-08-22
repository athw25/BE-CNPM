# src/app_logging.py
import logging
import sys
import uuid
from typing import Optional
from flask import has_request_context, request

_REQUEST_ID_HEADER = "X-Request-ID"


class RequestIdFilter(logging.Filter):
    """Gắn request_id vào log record nếu đang ở trong context HTTP."""
    def filter(self, record: logging.LogRecord) -> bool:
        if has_request_context():
            rid = request.headers.get(_REQUEST_ID_HEADER) or request.environ.get("request_id")
        else:
            rid = None
        record.request_id = rid or "-"
        return True


def init_logging(level: str = "INFO") -> None:
    """Cấu hình logging toàn cục, output ra stdout, có request_id."""
    root = logging.getLogger()
    if root.handlers:
        # tránh add lặp
        return

    root.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | rid=%(request_id)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    handler.setFormatter(formatter)
    handler.addFilter(RequestIdFilter())
    root.addHandler(handler)


def ensure_request_id(environ: dict) -> None:
    """Đảm bảo mỗi request có 1 request_id — dùng trong middleware sớm."""
    rid = environ.get("HTTP_" + _REQUEST_ID_HEADER.replace("-", "_"))
    if not rid:
        environ["request_id"] = str(uuid.uuid4())
