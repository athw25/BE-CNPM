import time
import uuid
from flask import g, request

def init_middleware(app):
    @app.before_request
    def _before():
        # Gán request_id
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        g._start_ts = time.time()

    @app.after_request
    def _after(resp):
        # Tính latency và gắn header
        try:
            latency_ms = int((time.time() - getattr(g, "_start_ts", time.time())) * 1000)
        except Exception:
            latency_ms = -1

        resp.headers["X-Request-ID"] = getattr(g, "request_id", "-")
        resp.headers["X-Response-Time"] = f"{latency_ms}ms"

        # Log nhanh (dựa vào logging.py đã thêm filter request_id)
        try:
            app.logger.info("HTTP %s %s -> %s (%sms)",
                            request.method, request.path, resp.status_code, latency_ms)
        except Exception:
            pass
        return resp

# -------- Optional: JWT/RBAC (cần pip install PyJWT) --------
# from functools import wraps
# import os, jwt
#
# def require_jwt(roles: set[str] | None = None):
#     secret = os.getenv("JWT_SECRET", "dev-secret")
#
#     def decorator(fn):
#         @wraps(fn)
#         def wrapper(*args, **kwargs):
#             auth = request.headers.get("Authorization", "")
#             if not auth.startswith("Bearer "):
#                 return {"error": "Missing Bearer token"}, 401
#             token = auth.split(" ", 1)[1]
#             try:
#                 claims = jwt.decode(token, secret, algorithms=["HS256"])
#                 g.jwt_claims = claims
#             except Exception:
#                 return {"error": "Invalid token"}, 401
#             if roles:
#                 user_role = claims.get("role")
#                 if user_role not in roles:
#                     return {"error": "Forbidden"}, 403
#             return fn(*args, **kwargs)
#         return wrapper
#     return decorator
