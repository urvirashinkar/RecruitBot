from pydantic import BaseModel
from typing import List, Optional

# --- UI-Facing Models ---
class ExperienceShort(BaseModel):
    job_title: str
    company: str

class CandidateShort(BaseModel):
    id: str
    name: str
    summary: str
    skills: List[str]
    experience: List[ExperienceShort]

# --- Full Candidate Schema for MongoDB ---
class PersonalInfo(BaseModel):
    full_name: str
    email: str
    phone: str
    linkedin: str
    github: str
    portfolio: str
    address: str
    summary: str

class Education(BaseModel):
    degree: str
    major: str
    university: str
    location: str
    start_date: str
    end_date: str
    gpa: str

class Experience(BaseModel):
    job_title: str
    company: str
    location: str
    start_date: str
    end_date: str
    responsibilities: List[str]
    technologies_used: List[str]

class Project(BaseModel):
    project_name: str
    description: str
    technologies: List[str]
    link: str

class Skills(BaseModel):
    technical: List[str]
    soft: List[str]
    languages: List[str]

class Certification(BaseModel):
    name: str
    issuing_organization: str
    issue_date: str
    expiration_date: Optional[str] = None
    credential_id: str
    credential_url: str

class Publication(BaseModel):
    title: str
    journal: str
    date: str
    url: str

class VolunteerExperience(BaseModel):
    role: str
    organization: str
    start_date: str
    end_date: str
    description: str

class AdditionalInfo(BaseModel):
    interests: List[str]
    volunteer_experience: List[VolunteerExperience]

class CandidateMongo(BaseModel):
    personal_info: PersonalInfo
    education: List[Education]
    experience: List[Experience]
    projects: List[Project]
    skills: Skills
    certifications: List[Certification]
    achievements: List[str]
    publications: List[Publication]
    additional_info: AdditionalInfo

class CandidateIn(BaseModel):
    candidate: CandidateMongo

