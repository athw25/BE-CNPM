from flask import jsonify

# Nếu bạn có exceptions riêng, import ở đây
class DomainError(Exception): ...
class ValidationError(DomainError): ...
class NotFoundError(DomainError): ...
class ConflictError(DomainError): ...

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(NotFoundError)
    def handle_not_found(e):
        return jsonify({"error": str(e)}), 404

    @app.errorhandler(ConflictError)
    def handle_conflict(e):
        return jsonify({"error": str(e)}), 409

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad Request"}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(Exception)
    def unhandled(e):
        # chỉ log chung, không lộ stacktrace ra ngoài
        app.logger.exception(e)
        return jsonify({"error": "Internal Server Error"}), 500
