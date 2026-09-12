# Day 1 Workflow

## What

Establish the Django, FastAPI, and React service boundaries; configure PostgreSQL/Redis settings; implement custom-user JWT authentication; and add the first health checks.

## How

Django owns identity and authorization. FastAPI exposes an isolated health endpoint for future AI workloads. React consumes Django through Axios and protects the dashboard using the access token.

## Why

Authentication and service boundaries are foundational dependencies for every later HireFlow feature.

## Verification

- Django migrations complete successfully.
- Four authentication tests pass through Django's test runner.
- FastAPI health test passes through pytest.
- Frontend build is pending because npm dependencies could not be materialized in the current environment.
