# HireFlow AI

AI-powered recruitment and applicant tracking platform connecting candidates, recruiters, companies, jobs, applications, interviews, and explainable AI assistance.

## Project status

Days 1–7 are complete for the local-development scope. Day 7 adds responsive UI polish, health/readiness checks, security defaults, structured logging, CI, Docker healthchecks, repeatable demo data, and release documentation.

Managed cloud deployment remains outside this local project scope.

## Technology stack

- React, TypeScript, Vite, React Router, Axios, TanStack Query
- Django and Django REST Framework
- FastAPI for AI workloads
- PostgreSQL in production
- Redis and Celery for asynchronous processing
- Django Channels for real-time events
- Docker Compose is optional for team/deployment environments.

## Repository guide

- `backend/`: Django modular monolith
- `ai-service/`: FastAPI AI boundary
- `frontend/`: React application
- `infrastructure/`: Docker, Nginx, and operational scripts
- `docs/`: architecture, setup, daily records, tests, and walkthroughs

## Quick start

Docker is not required for Day 1. Start Django, FastAPI, and React separately; development settings use SQLite when PostgreSQL is not configured. Detailed commands are in [`docs/Walk Through/`](docs/Walk%20Through/) and [`docs/development-setup.md`](docs/development-setup.md).

## Verification

Backend: `python manage.py check` and `python manage.py test apps.accounts.tests -v 1`.

AI service: `python -m pytest -q` from `ai-service`.

Frontend: `npm test`, `npm run build`, and `npm run test:e2e` from `frontend` after installing Chromium with `npx playwright install chromium`.

## Documentation

Start with [`docs/README.md`](docs/README.md), then review [`docs/architecture.md`](docs/architecture.md), [`docs/authentication.md`](docs/authentication.md), and the daily workflow records.
