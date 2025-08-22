# src/dependency_container.py
from infrastructure.databases import SessionLocal
# Import repository
from infrastructure.repositories.identity_repository import UserRepository, InternRepository
from infrastructure.repositories.recruitment_repository import CampaignRepository, ApplicationRepository
from infrastructure.repositories.training_repository import ProgramRepository, ProjectRepository
from infrastructure.repositories.work_repository import AssignmentRepository
from infrastructure.repositories.evaluation_repository import EvaluationRepository

# Import service
from services.identity_service import IdentityService
from services.recruitment_service import RecruitmentService
from services.training_service import TrainingService
from services.work_service import WorkService
from services.evaluation_service import EvaluationService


# ----------- Repositories -----------
db_session = SessionLocal()

user_repository = UserRepository(db_session)
intern_repository = InternRepository(db_session)

campaign_repository = CampaignRepository(db_session)
application_repository = ApplicationRepository(db_session)

program_repository = ProgramRepository(db_session)
project_repository = ProjectRepository(db_session)

assignment_repository = AssignmentRepository(db_session)

evaluation_repository = EvaluationRepository(db_session)


# ----------- Services -----------
identity_service = IdentityService(
    user_repo=user_repository,
    intern_repo=intern_repository,
)

recruitment_service = RecruitmentService(
    campaign_repo=campaign_repository,
    application_repo=application_repository,
)

training_service = TrainingService(
    program_repo=program_repository,
    project_repo=project_repository,
)

work_service = WorkService(
    assignment_repo=assignment_repository,
)

evaluation_service = EvaluationService(
    evaluation_repo=evaluation_repository,
)
