from dataclasses import dataclass

@dataclass
class CreateProjectDTO:
    progID: int
    title: str

@dataclass
class UpdateProjectDTO:
    title: str | None = None

@dataclass
class ProjectResponseDTO:
    projID: int
    progID: int
    title: str
