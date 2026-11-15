import re

from django.db import transaction
from django.utils import timezone

from apps.candidates.models import CandidateProfile, Resume
from apps.jobs.models import Job
from .models import MatchResult


STOP_WORDS = {"and", "the", "with", "for", "this", "that", "from", "you", "your", "are", "will", "our"}


def _tokens(value):
    return {word for word in re.findall(r"[a-z0-9+#.]+", (value or "").lower()) if word not in STOP_WORDS and len(word) > 2}


def candidate_context(candidate):
    profile, _ = CandidateProfile.objects.get_or_create(user=candidate)
    resume = Resume.objects.filter(candidate=candidate, status=Resume.Status.READY).first()
    analysis = resume.analysis if resume else {}
    skills = {str(skill).strip().lower() for skill in analysis.get("skills", []) if str(skill).strip()}
    resume_text = resume.extracted_text if resume else ""
    return profile, skills, resume_text


def calculate_match(candidate, job):
    profile, candidate_skills, resume_text = candidate_context(candidate)
    job_skills = {skill.name.strip().lower() for skill in job.skills.all()}
    matched = sorted(candidate_skills & job_skills)
    missing = sorted(job_skills - candidate_skills)
    skill_score = round((len(matched) / len(job_skills)) * 60) if job_skills else 60
    experience_score = 20 if profile.years_experience >= job.min_experience else round((profile.years_experience / max(job.min_experience, 1)) * 20)
    job_tokens = _tokens(f"{job.title} {job.description}")
    resume_tokens = _tokens(resume_text)
    semantic_score = round((len(job_tokens & resume_tokens) / len(job_tokens)) * 20) if job_tokens else 0
    score = max(0, min(100, skill_score + experience_score + semantic_score))
    return {
        "score": score,
        "skill_score": max(0, min(60, skill_score)),
        "experience_score": max(0, min(20, experience_score)),
        "semantic_score": max(0, min(20, semantic_score)),
        "matched_skills": matched,
        "missing_skills": missing,
        "explanation": {
            "weights": {"skills": 60, "experience": 20, "semantic_similarity": 20},
            "summary": f"Matched {len(matched)} of {len(job_skills)} required skills; {len(missing)} skill gaps identified.",
        },
    }


@transaction.atomic
def create_or_update_match(candidate, job):
    values = calculate_match(candidate, job)
    match, _ = MatchResult.objects.update_or_create(candidate=candidate, job=job, defaults=values)
    return match


def recommendation_queryset(candidate):
    applied_job_ids = candidate.applications.values_list("job_id", flat=True)
    return Job.objects.filter(status=Job.Status.PUBLISHED).exclude(id__in=applied_job_ids).prefetch_related("skills")
