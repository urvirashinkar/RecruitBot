import os
from sentence_transformers import SentenceTransformer

# Load model once
_model = None
def get_model():
    global _model
    if _model is None:
        model_name = os.getenv("EMBEDDING_MODEL", "all-mpnet-base-v2")
        _model = SentenceTransformer(model_name)
    return _model

def get_embedding(text: str):
    model = get_model()
    return model.encode([text])[0].tolist()

def flatten_candidate(candidate: dict) -> str:
    """
    Flatten the candidate schema into a single string for embedding.
    """
    parts = []
    pi = candidate.get("personal_info", {})
    parts.append(f"Name: {pi.get('full_name','')}")
    parts.append(f"Summary: {pi.get('summary','')}")
    parts.append(f"Email: {pi.get('email','')}")
    parts.append(f"Phone: {pi.get('phone','')}")
    parts.append(f"LinkedIn: {pi.get('linkedin','')}")
    parts.append(f"GitHub: {pi.get('github','')}")
    parts.append(f"Portfolio: {pi.get('portfolio','')}")
    parts.append(f"Address: {pi.get('address','')}")
    # Education
    for edu in candidate.get("education", []):
        parts.append(f"Education: {edu.get('degree','')} in {edu.get('major','')} at {edu.get('university','')} ({edu.get('start_date','')} - {edu.get('end_date','')}) GPA: {edu.get('gpa','')}")
    # Experience
    for exp in candidate.get("experience", []):
        parts.append(f"Experience: {exp.get('job_title','')} at {exp.get('company','')} ({exp.get('start_date','')} - {exp.get('end_date','')}) Responsibilities: {'; '.join(exp.get('responsibilities', []))} Technologies: {', '.join(exp.get('technologies_used', []))}")
    # Projects
    for proj in candidate.get("projects", []):
        parts.append(f"Project: {proj.get('project_name','')} - {proj.get('description','')} Technologies: {', '.join(proj.get('technologies', []))} Link: {proj.get('link','')}")
    # Skills
    skills = candidate.get("skills", {})
    parts.append(f"Technical Skills: {', '.join(skills.get('technical', []))}")
    parts.append(f"Soft Skills: {', '.join(skills.get('soft', []))}")
    parts.append(f"Languages: {', '.join(skills.get('languages', []))}")
    # Certifications
    for cert in candidate.get("certifications", []):
        parts.append(f"Certification: {cert.get('name','')} by {cert.get('issuing_organization','')} ({cert.get('issue_date','')} - {cert.get('expiration_date','')}) Credential: {cert.get('credential_id','')} {cert.get('credential_url','')}")
    # Achievements
    for ach in candidate.get("achievements", []):
        parts.append(f"Achievement: {ach}")
    # Publications
    for pub in candidate.get("publications", []):
        parts.append(f"Publication: {pub.get('title','')} in {pub.get('journal','')} ({pub.get('date','')}) {pub.get('url','')}")
    # Additional Info
    add = candidate.get("additional_info", {})
    for interest in add.get("interests", []):
        parts.append(f"Interest: {interest}")
    for vol in add.get("volunteer_experience", []):
        parts.append(f"Volunteer: {vol.get('role','')} at {vol.get('organization','')} ({vol.get('start_date','')} - {vol.get('end_date','')}) {vol.get('description','')}")
    return "\n".join(parts)