# Day 1 Pytest Cases

The AI-service health test passes with pytest. Django authentication tests pass with Django's built-in test runner because pytest-django is not installed in the current environment. Frontend authentication tests pass with Vitest.

| ID | Scenario | Result |
|---|---|---|
| AUTH-001 | Candidate registration | PASS |
| AUTH-002 | Public administrator registration rejected | PASS |
| AUTH-003 | Login, current-user, and logout | PASS |
| AUTH-004 | Unauthenticated current-user request | PASS |
| AUTH-005 | Duplicate email rejected | PASS |
| AUTH-006 | Password confirmation mismatch rejected | PASS |
| AI-001 | AI service health endpoint | PASS |
| UI-001 | Login and registration component rendering/validation | PASS: 3 Vitest tests |
