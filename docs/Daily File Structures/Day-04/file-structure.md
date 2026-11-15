# Day 4 File Structure

Delivered changes:

- `backend/apps/candidates/models.py`: private `Resume` lifecycle and stored analysis fields.
- `backend/apps/candidates/serializers.py`: size, extension, empty-file, and executable upload validation.
- `backend/apps/candidates/resume_services.py`: text extraction and FastAPI client fallback.
- `backend/apps/candidates/tasks.py`: retryable processing task with local development fallback.
- `backend/apps/candidates/resume_urls.py`: authenticated resume API routes.
- `backend/apps/candidates/migrations/0002_resume.py`: resume schema migration.
- `backend/apps/candidates/tests/test_resumes.py`: Day 4 workflow coverage.
- `ai-service/app/main.py`: resume analysis endpoint.
