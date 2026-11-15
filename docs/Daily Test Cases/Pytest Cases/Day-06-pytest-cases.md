# Day 6 Pytest/API Test Cases

Automated coverage is in `backend/apps/interviews/tests/test_day6.py`.

| Case | Expected result |
|---|---|
| Recruiter schedules interview | HTTP 201 and candidate notification |
| Foreign interview access | HTTP 404 |
| Conversation message | HTTP 201 and recipient notification |
| Message read state | `read_at` is recorded |
| Dashboard metrics | Candidate/recruiter data is role and company scoped |
| WebSocket | JWT and participant membership are required by the consumer |

Command: `python manage.py test apps.interviews.tests.test_day6 -v 1`.
