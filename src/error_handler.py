# src/error_handler.py
import logging
import uuid
from typing import Tuple, Any, Dict

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)

# Nếu bạn có domain exceptions riêng, import vào đây
try:
    from src.domain.exceptions import ValidationError, NotFoundError, DomainError
except Exception:
    # fallback khi chưa tạo
    class DomainError(Exception): ...
    class ValidationError(DomainError): ...
    class NotFoundError(DomainError): ...


def _make_problem(status: int, title: str, detail: str = "", code: str = "") -> Tuple[Dict[str, Any], int]:
    # Lấy/gán traceId & requestId
    trace_id = request.headers.get("X-Request-ID") or request.environ.get("request_id") or str(uuid.uuid4())
    problem = {
        "type": "about:blank",
        "title": title,
        "status": status,
        "detail": detail,
        "traceId": trace_id,
        "code": code or "",
    }
    return problem, status


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_exception(err: HTTPException):
        logger.warning("HTTPException: %s", err)
        problem, status = _make_problem(
            status=err.code or 500,
            title=err.name,
            detail=err.description,
            code="HTTP_ERROR",
        )
        return jsonify(problem), status

    @app.errorhandler(ValidationError)
    def handle_validation(err: ValidationError):
        logger.info("ValidationError: %s", err)
        problem, status = _make_problem(
            status=422,
            title="Validation failed",
            detail=str(err),
            code="VALIDATION_ERROR",
        )
        return jsonify(problem), status

    @app.errorhandler(NotFoundError)
    def handle_not_found(err: NotFoundError):
        logger.info("NotFoundError: %s", err)
        problem, status = _make_problem(
            status=404,
            title="Resource not found",
            detail=str(err),
            code="NOT_FOUND",
        )
        return jsonify(problem), status

    @app.errorhandler(DomainError)
    def handle_domain(err: DomainError):
        logger.warning("DomainError: %s", err)
        problem, status = _make_problem(
            status=409,
            title="Business rule violation",
            detail=str(err),
            code="DOMAIN_ERROR",
        )
        return jsonify(problem), status

    @app.errorhandler(Exception)
    def handle_unknown(err: Exception):
        logger.exception("Unhandled exception")
        problem, status = _make_problem(
            status=500,
            title="Internal Server Error",
            detail="An unexpected error occurred.",
            code="INTERNAL_ERROR",
        )
        return jsonify(problem), status
