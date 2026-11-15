# Testing Strategy

## Test layers

- Unit tests for models, services, scoring, and validators.
- API tests for status codes, payloads, authentication, and permissions.
- Database tests for constraints and transactions.
- Celery task tests for retries and failure states.
- FastAPI tests for extraction and AI endpoints.
- React tests for forms, routes, loading, and error states.
- Playwright tests for critical end-to-end flows.

## Current verification commands

```cmd
cd frontend
npm ci
npm test
npm run build
npx playwright install chromium
npm run test:e2e
```

The browser suite covers authentication-page rendering, required-field validation, and login-to-registration navigation. API and model security tests cover role isolation, IDOR-style access attempts, protected resume uploads, invalid application transitions, and company membership boundaries.

## Day 1 evidence

- Django system check passed.
- Django migrations passed.
- Six authentication tests passed using `python manage.py test apps.accounts.tests -v 1`.
- FastAPI health test passed using pytest.
- Frontend TypeScript/Vite production build passed after dependencies were installed.
- Frontend authentication component tests passed: 3 tests.
- Docker runtime was not tested because Docker is intentionally optional for this project workflow.

## Day 4 evidence

- Backend system checks and full Django suite passed: 14 tests.
- Resume workflow tests cover validation, ownership, successful text processing, and failure recording.
- FastAPI health test passed: 1 test.
- Playwright/browser verification is not installed and is not claimed as executed.

## Required future workflows

Registration, login, job publishing, application submission, invalid status transition, AI matching, notifications, interview scheduling, and role isolation.

Tests must report actual results. Do not document a feature as passing until its test has run.
