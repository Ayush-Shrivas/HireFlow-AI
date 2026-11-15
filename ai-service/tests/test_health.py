import pytest
from fastapi import HTTPException

from app.main import ResumeAnalysisRequest, analyze_resume, health


def test_health():
    assert health() == {"status": "ok", "service": "ai-service"}


def test_resume_analysis_extracts_skills_and_experience():
    payload = analyze_resume(
        ResumeAnalysisRequest(
            filename="resume.txt",
            text="Python and Django engineer with 6 years experience. Bachelor degree. engineer@example.com",
        )
    )
    assert payload["skills"] == ["python", "django"]
    assert payload["years_experience"] == 6
    assert payload["confidence"] > 0.5
    assert payload["sections"]["has_contact_email"] is True


def test_resume_analysis_rejects_invalid_service_token(monkeypatch):
    monkeypatch.setenv("AI_SERVICE_TOKEN", "expected")
    with pytest.raises(HTTPException) as error:
        analyze_resume(ResumeAnalysisRequest(text="Python"), x_service_token="wrong")
    assert error.value.status_code == 401
