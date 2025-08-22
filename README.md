# Project IMS

```bash
├─ README.md
├─ .env                               # MYSQL_URL=mysql+pymysql://root:1234@127.0.0.1:3306/ims?charset=utf8mb4
├─ .venv/                             # virtual env (local)
└─ src/
   ├─ __init__.py
   ├─ create_app.py                   # khởi tạo app + Base.metadata.create_all()
   ├─ enums.py                        # Role, CampaignStatus, ApplicationStatus, AssignmentStatus, ...
   │
   ├─ api/
   │  ├─ __init__.py
   │  ├─ controllers/                 # HTTP controllers (Flask Blueprint)
   │  │  ├─ user_controller.py
   │  │  ├─ intern_controller.py
   │  │  ├─ recruitment_controller.py
   │  │  ├─ application_controller.py
   │  │  ├─ training_controller.py
   │  │  ├─ project_controller.py
   │  │  ├─ assignment_controller.py
   │  │  └─ evaluation_controller.py
   │  ├─ schemas/                     # Marshmallow schemas (validate + serialize)
   │  │  ├─ user_schema.py
   │  │  ├─ intern_schema.py
   │  │  ├─ recruitment_schema.py
   │  │  ├─ application_schema.py
   │  │  ├─ training_schema.py
   │  │  ├─ project_schema.py
   │  │  ├─ assignment_schema.py
   │  │  └─ evaluation_schema.py
   │  ├─ middleware.py                # JWT/RBAC (tùy chọn), logging, request-id
   │  ├─ responses.py                 # chuẩn hóa JSON success/error
   │  └─ requests.py                  # helpers trích dữ liệu request, paging, filter
   │
   ├─ domain/                         # lớp Domain (logic thuần, không phụ thuộc ORM/Flask)
   │  ├─ __init__.py
   │  ├─ constants.py                 # hằng số nghiệp vụ (VD: MAX_TASK_DOING=3)
   │  ├─ exceptions.py                # DomainError, ValidationError, NotFoundError...
   │  ├─ models/                      # Domain Models (dataclass)
   │  │  ├─ user.py
   │  │  ├─ intern.py
   │  │  ├─ recruitment.py
   │  │  ├─ application.py
   │  │  ├─ training.py
   │  │  ├─ project.py
   │  │  ├─ assignment.py
   │  │  └─ evaluation.py
   │  └─ dtos/                        # DTO vào/ra Service (nếu cần tách riêng API DTO)
   │     ├─ user_dto.py
   │     ├─ intern_dto.py
   │     ├─ recruitment_dto.py
   │     ├─ application_dto.py
   │     ├─ training_dto.py
   │     ├─ project_dto.py
   │     ├─ assignment_dto.py
   │     └─ evaluation_dto.py
   │
   ├─ services/                       # Use case layer (gọi repository + áp quy tắc nghiệp vụ)
   │  ├─ __init__.py
   │  ├─ identity_service.py          # User, InternProfile
   │  ├─ recruitment_service.py       # RecruitmentCampaign, Application
   │  ├─ training_service.py          # TrainingProgram, Project
   │  ├─ work_service.py              # Assignment
   │  └─ evaluation_service.py        # Evaluation
   │
   ├─ infrastructure/
   │  ├─ __init__.py
   │  ├─ databases/
   │  │  ├─ __init__.py               # re-export: engine, Base, SessionLocal
   │  │  └─ db_base.py                # tạo Engine, Base = declarative_base(), SessionLocal
   │  ├─ models/                      # SQLAlchemy ORM (mapping DB) — CHÍNH LÀ nơi bạn đã gom sẵn
   │  │  ├─ __init__.py
   │  │  ├─ identity_models.py        # User, InternProfile
   │  │  ├─ recruitment_models.py     # RecruitmentCampaign, Application
   │  │  ├─ training_models.py        # TrainingProgram, Project
   │  │  ├─ work_models.py            # Assignment
   │  │  └─ evaluation_models.py      # Evaluation
   │  ├─ repositories/                # CRUD/Query tới DB, map ORM ↔ Domain
   │  │  ├─ __init__.py
   │  │  ├─ identity_repository.py    # UserRepository, InternRepository
   │  │  ├─ recruitment_repository.py # CampaignRepository, ApplicationRepository
   │  │  ├─ training_repository.py    # ProgramRepository, ProjectRepository
   │  │  ├─ work_repository.py        # AssignmentRepository
   │  │  └─ evaluation_repository.py  # EvaluationRepository
   │  └─ services/
   │     ├─ __init__.py
   │     └─ email_service.py          # ví dụ service hạ tầng (tùy chọn)
   │
   ├─ dependency_container.py         # wiring DI: khởi tạo repo/service, inject vào controller
   ├─ error_handler.py                # bắt và trả JSON lỗi chuẩn cho toàn app
   ├─ logging.py                      # cấu hình logging
   └─ cors.py                         # bật CORS nếu cần
```