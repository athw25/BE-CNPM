# src/api/schemas/project_schema.py
from typing import Optional
from pydantic import BaseModel, Field, validator

# ------------ Request DTOs ------------

class CreateProjectDTO(BaseModel):
    progID: int = Field(..., description="ID của TrainingProgram cha")
    title: str = Field(..., min_length=1, max_length=120, description="Tên project")

    @validator("title")
    def _strip_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("title cannot be empty")
        return v


class UpdateProjectDTO(BaseModel):
    # Cho phép cập nhật 1 phần (partial update)
    progID: Optional[int] = Field(None, description="ID của TrainingProgram cha")
    title: Optional[str] = Field(None, min_length=1, max_length=120, description="Tên project")

    @validator("title")
    def _strip_title(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("title cannot be empty")
        return v


# ------------ Response DTO ------------

class ProjectResponseDTO(BaseModel):
    projID: int
    progID: int
    title: str


# ------------ (Tuỳ chọn) Query DTO cho list/filter ------------

class ProjectQueryDTO(BaseModel):
    progID: Optional[int] = None
    q: Optional[str] = Field(None, description="Tìm theo từ khoá trong title (tuỳ controller áp dụng)")
    page: Optional[int] = Field(1, ge=1)
    page_size: Optional[int] = Field(50, ge=1, le=200)
