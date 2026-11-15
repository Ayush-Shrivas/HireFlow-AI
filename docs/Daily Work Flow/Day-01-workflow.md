# Day 1 Workflow

## What

Establish the Django, FastAPI, and React service boundaries; configure PostgreSQL/Redis settings; implement custom-user JWT authentication; and add the first health checks.

## How

Django owns identity and authorization. FastAPI exposes an isolated health endpoint for future AI workloads. React consumes Django through Axios and protects the dashboard using the access token.

## Why

Authentication and service boundaries are foundational dependencies for every later HireFlow feature.

## Files and services delivered

- Django custom email-based user model with candidate, recruiter, and administrator roles.
- JWT registration, login, refresh, logout, and current-user endpoints.
- PostgreSQL-compatible configuration with SQLite fallback for local Day 1 work.
- FastAPI `/health` endpoint.
- React login, registration, protected dashboard, and logout flows.
- Automated backend, AI-service, and frontend tests.
- Optional Dockerfiles and Compose configuration.

## Verification results

- Django system check: PASS.
- Django migrations: PASS.
- Django authentication suite: PASS, 6 tests.
- FastAPI pytest suite: PASS, 1 test.
- Frontend Vitest suite: PASS, 3 tests.
- Frontend TypeScript/Vite production build: PASS.
- Docker Compose YAML syntax: PASS.
- Docker runtime: intentionally not executed because Docker is not part of the selected workflow.
- Playwright browser report: not generated; Playwright is scheduled for later end-to-end coverage.

## Completion

Day 1 is complete at 100% for the approved local-development scope. Day 2 begins with candidate profiles, companies, skills, and jobs.
