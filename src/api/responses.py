from flask import jsonify

def ok(data=None, message="Success", status=200):
    return jsonify({"data": data, "error": None, "message": message}), status

def created(data=None, message="Created"):
    return ok(data, message, status=201)

def err(message="Bad Request", status=400, code=None):
    body = {"data": None, "error": code or "ERROR", "message": message}
    return jsonify(body), status
