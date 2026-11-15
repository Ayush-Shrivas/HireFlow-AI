import os
import re

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="HireFlow AI Service", version="0.1.0")

class ResumeAnalysisRequest(BaseModel):
    text: str
    filename: str = "resume"

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ai-service"}

@app.get("/health/ready")
def readiness() -> dict[str, str]:
    return {"status": "ready", "service": "ai-service"}

@app.post("/v1/resumes/analyze")
def analyze_resume(payload: ResumeAnalysisRequest, x_service_token: str | None = Header(default=None)) -> dict:
    configured_token = os.getenv("AI_SERVICE_TOKEN", "")
    if configured_token and x_service_token != configured_token:
        raise HTTPException(status_code=401, detail="Invalid service token")
    text = re.sub(r"\s+", " ", payload.text).strip()
    normalized = text.lower()
    skill_aliases = {
        "python": ("python",),
        "django": ("django",),
        "fastapi": ("fastapi",),
        "react": ("react", "reactjs"),
        "typescript": ("typescript",),
        "javascript": ("javascript", "js"),
        "sql": ("sql", "postgres", "mysql", "database"),
        "docker": ("docker", "containerization"),
        "aws": ("aws", "amazon web services"),
        "git": ("git", "github", "gitlab"),
        "kubernetes": ("kubernetes", "k8s"),
    }
    skills = [skill for skill, aliases in skill_aliases.items() if any(re.search(rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])", normalized) for alias in aliases)]
    experience_matches = [int(value) for value in re.findall(r"(?<!\d)(\d{1,2})\+?\s*(?:years?|yrs?)", normalized)]
    years_experience = min(max(experience_matches or [0]), 50)
    sections = {
        "has_contact_email": bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)),
        "has_education": any(term in normalized for term in ("bachelor", "master", "b.tech", "degree", "university")),
        "has_work_history": any(term in normalized for term in ("experience", "worked", "employment", "career")),
    }
    confidence = round(min(0.98, 0.45 + (0.08 * len(skills)) + (0.1 if sections["has_work_history"] else 0)), 2)
    summary = f"Extracted {len(text.split())} words from {payload.filename}; detected {len(skills)} supported skills."
    return {
        "skills": skills,
        "years_experience": years_experience,
        "summary": summary,
        "confidence": confidence,
        "sections": sections,
    }
