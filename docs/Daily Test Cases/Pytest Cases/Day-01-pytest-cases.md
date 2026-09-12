# Day 1 Pytest Cases

The AI-service health test passes with pytest. Django authentication tests pass with Django's built-in test runner because pytest-django is not installed in the current environment.

| ID | Scenario | Result |
|---|---|---|
| AUTH-001 | Candidate registration | PASS |
| AUTH-002 | Public administrator registration rejected | PASS |
| AUTH-003 | Login, current-user, and logout | PASS |
| AUTH-004 | Unauthenticated current-user request | PASS |
| AI-001 | AI service health endpoint | PASS |
