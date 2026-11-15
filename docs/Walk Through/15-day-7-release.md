# Day 7 Release Walkthrough

## Seed local demo data

From `backend`, run `python manage.py migrate` followed by `python manage.py seed_demo`.

The command creates demo recruiter and candidate accounts using `DemoPass123!`, a company, skills, and a published Product Engineer role.

## Validate services

Run `python manage.py check`, `python manage.py test -v 1`, `python -m pytest -q`, `npm test -- --run`, and `npm run build`.

Health endpoints are `http://localhost:8000/health/`, `http://localhost:8000/health/ready/`, and `http://localhost:8001/health/ready`.

## Container validation

Run `docker compose config`, `docker compose build`, and `docker compose up` when Docker is installed. Compose healthchecks target the backend, AI service, and frontend.