from datetime import date
from enum import Enum
from typing import Annotated, ClassVar, Literal, override

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator


def handle_empty_date(v: str | date | None) -> date | str | None:
    if v == "":
        return None
    return v


DateOrPresent = Annotated[date | Literal["present"] | None, BeforeValidator(handle_empty_date)]

class StrEnum(str, Enum):
    @override
    def __str__(self) -> str:
        return str.__str__(self)


class SkillLevel(StrEnum):
    advanced = "Advanced"
    master = "Master"


class StudyType(StrEnum):
    bachelors = "Bachelors"


class ProjectType(StrEnum):
    application = "Application"
    python_package = "Python Package"


class Model(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        str_strip_whitespace=True,
        use_enum_values=True,
    )


class Location(Model):
    """Geographic location information."""
    address: str | None = None
    postal_code: str = Field(alias="postalCode", examples=["27529", "NC 27529"])
    city: str = Field(examples=["Garner", "Raleigh"])
    country_code: str = Field(alias="countryCode", description="ISO country code", examples=["US"])
    region: str = Field(description="State or region name", examples=["North Carolina", "California"])


class Profile(Model):
    """Social media or professional network profile."""
    network: str = Field(description="Name of the social network or platform", examples=["GitHub", "LinkedIn", "Kaggle"])
    username: str | None = None
    url: str = Field(description="Full URL to the profile", examples=["https://github.com/estasney"])
    handle: str = Field(description="Display handle or identifier", examples=["estasney", "eric-stasney"])
    icon: str = Field(description="CSS class for icon display", examples=["fab fa-github", "fab fa-linkedin"])


class Basics(Model):
    """Basic personal and contact information."""
    name: str = Field(examples=["Eric Stasney"])
    label: str = Field(description="Professional title or role", examples=["Full Stack Data Engineer", "Data Scientist"])
    image: str | None = None
    email: str | None = None
    phone: str | None = None
    url: str = Field(description="Primary professional URL", examples=["https://www.linkedin.com/in/eric-stasney"])
    summary: str = Field(description="Professional summary or bio")
    location: Location
    profiles: list[Profile]


class Work(Model):
    """Work experience entry."""
    name: str = Field(description="Company or organization name", examples=["Cisco Systems", "US Army / COARNG"])
    location: str = Field(description="Work location (city, state, remote status)", examples=["Raleigh, NC (Remote)", "Denver, CO"])
    description: str = Field(description="Department or division", examples=["Customer Lifecycle Operations", "Talent Hub"])
    position: str = Field(description="Job title", examples=["Data Architect", "Data Scientist", "Software Engineer"])
    url: str | None = None
    start_date: DateOrPresent = Field(alias="startDate", examples=["Nov 2025", "2023-01-15"])
    end_date: DateOrPresent = Field(default=None, alias="endDate", description="End date or 'present' for current position", examples=["Present", "Nov 2025", "2025-11-30"])
    summary: str | None = Field(default=None, description="Brief role summary")
    highlights: list[str] = Field(description="Key achievements and responsibilities")
    display: bool = Field(default=False, description="Whether to display this work item expanded by default")



class Education(Model):
    """Educational background entry."""
    institution: str = Field(description="Name of educational institution", examples=["The University of Tennessee", "MIT"])
    area: str = Field(description="Field of study or major", examples=["Biochemistry, Cellular and Molecular Biology", "Computer Science"])
    study_type: StudyType = Field(alias="studyType", description="Degree type")
    start_date: date = Field(alias="startDate", examples=["2006", "2006-08-15"])
    end_date: date = Field(alias="endDate", examples=["2011", "2011-05-20"])


class Skill(Model):
    """Technical or professional skill with proficiency level."""
    name: str = Field(description="Skill category or area", examples=["API Development", "Web Development", "Containerization & DevOps"])
    level: SkillLevel = Field(description="Proficiency level")
    keywords: list[str] = Field(description="Specific technologies or tools within this skill", examples=[["Pydantic", "FastAPI", "OpenAPI/Swagger"]])

    @model_validator(mode="after")
    def deduplicate_keywords(self) -> "Skill":
        """Remove duplicate keywords while maintaining order."""
        seen = set()
        deduplicated = []
        for keyword in self.keywords:
            if keyword not in seen:
                seen.add(keyword)
                deduplicated.append(keyword)
        self.keywords = deduplicated
        return self


class Interest(Model):
    """Personal or professional interest area."""
    name: str = Field(description="Interest category", examples=["IoT & Robotics", "Electrical Engineering"])
    keywords: list[str] = Field(description="Specific topics or technologies of interest", examples=[["Arduino", "ESP32", "C++"]])


class Project(Model):
    """Personal or professional project entry."""
    name: str = Field(description="Project name", examples=["MindRef", "hNMF", "DupCheck"])
    description: str = Field(description="Brief project description", examples=["Cross-platform note taking application", "Hierarchical Non-Negative Matrix Factorization"])
    highlights: list[str] = Field(description="Key features, achievements, or technical details")
    keywords: list[str] = Field(description="Technologies, tools, or skills used", examples=[["Kivy", "GUI", "Android"], ["NumPy", "Scipy", "Scikit-learn"]])
    start_date: DateOrPresent | None = Field(default=None, alias="startDate", examples=["May 2022", "2022-05-15"])
    end_date: DateOrPresent | None = Field(default=None, alias="endDate", description="End date, 'present' for ongoing, or empty for completed", examples=["", "present", "Dec 2023"])
    url: str | None = Field(default=None, description="Project URL or repository link", examples=["https://github.com/estasney/MindRef"])
    type: ProjectType | None = Field(default=None, description="Project category")
    roles: list[str] | None = Field(default=None, description="Roles or responsibilities in the project", examples=[["Package Developer and Maintainer"]])
    entity: str | None = Field(default=None, description="Organization or entity associated with the project")



class Resume(Model):
    """Complete resume document structure matching me.yml format."""
    basics: Basics = Field(description="Personal and contact information")
    work: list[Work] = Field(description="Work experience history")
    education: list[Education] = Field(description="Educational background")
    skills: list[Skill] = Field(description="Technical and professional skills with proficiency levels")
    skills_ul: list[str] | None = Field(default=None, description="Unstructured list of additional skills")
    technologies: list[str] = Field(description="Flat list of technologies and tools")
    highlights: list[str] = Field(description="Key professional highlights and competencies")
    interests: list[Interest] = Field(description="Personal and professional interests")
    projects: list[Project] = Field(description="Notable projects and contributions")

    @model_validator(mode="after")
    def filter_skills_ul(self) -> "Resume":
        """Remove skills_ul items that appear as keywords in skills."""
        if not self.skills_ul:
            return self
        
        seen_in_skills = set()
        for skill in self.skills:
            seen_in_skills.update(skill.keywords)
        
        filtered = []
        for skill_item in self.skills_ul:
            if skill_item not in seen_in_skills:
                filtered.append(skill_item)
        
        self.skills_ul = filtered if filtered else None
        return self

