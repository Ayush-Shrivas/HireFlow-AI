# Day 4 Pytest/API Test Cases

Automated coverage is in `backend/apps/candidates/tests/test_resumes.py`.

| Case | Expected result |
|---|---|
| Candidate uploads TXT resume | HTTP 201 and processing reaches READY |
| Empty file | HTTP 400 |
| Unsupported/executable file | HTTP 400 |
| File over configured limit | HTTP 400 |
| Recruiter upload or foreign read | HTTP 403/404 |
| Empty extracted document | FAILED status and failure reason |

Command: `python manage.py test apps.candidates.tests.test_resumes -v 1`.
