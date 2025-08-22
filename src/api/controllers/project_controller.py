from flask import Blueprint, request, jsonify
from api.responses import success_response, error_response
from services.training_service import TrainingService
from api.schemas.project_schema import ProjectSchema
from dependency_container import project_repository
from domain.dtos.project_dto import ProjectCreateDTO, ProjectUpdateDTO

# Blueprint
project_bp = Blueprint("projects", __name__, url_prefix="/api/projects")

# Service (inject repository từ dependency_container)
project_service = TrainingService(project_repository)

# Schema (Marshmallow hoặc Pydantic tùy bạn cài)
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)


# ----------------------
# ROUTES
# ----------------------

@project_bp.route("/", methods=["GET"])
def list_projects():
    try:
        projects = project_service.get_all_projects()
        return success_response(projects_schema.dump(projects))
    except Exception as e:
        return error_response(str(e), 500)


@project_bp.route("/<int:project_id>", methods=["GET"])
def get_project(project_id):
    try:
        project = project_service.get_project_by_id(project_id)
        if not project:
            return error_response("Project not found", 404)
        return success_response(project_schema.dump(project))
    except Exception as e:
        return error_response(str(e), 500)


@project_bp.route("/", methods=["POST"])
def create_project():
    try:
        data = request.get_json()
        dto = ProjectCreateDTO(**data)   # Dùng DTO để validate input
        project = project_service.create_project(dto)
        return success_response(project_schema.dump(project), 201)
    except Exception as e:
        return error_response(str(e), 400)


@project_bp.route("/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    try:
        data = request.get_json()
        dto = ProjectUpdateDTO(**data)
        project = project_service.update_project(project_id, dto)
        return success_response(project_schema.dump(project))
    except Exception as e:
        return error_response(str(e), 400)


@project_bp.route("/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    try:
        project_service.delete_project(project_id)
        return success_response({"message": "Deleted successfully"})
    except Exception as e:
        return error_response(str(e), 400)
