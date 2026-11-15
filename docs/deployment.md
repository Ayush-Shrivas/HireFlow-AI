# Deployment Guide

## Target deployment

Use a managed PostgreSQL database, managed Redis, private object storage, and separate processes for Django, FastAPI, Celery worker, and Celery beat. Nginx terminates HTTPS and routes API, WebSocket, and frontend traffic.

## Required production configuration

- `DEBUG=False`.
- Strong secret values from a secret manager.
- HTTPS and secure cookies.
- Restricted CORS and allowed hosts.
- Database backups and migration procedure.
- Private resume storage.
- Health checks for Django, FastAPI, PostgreSQL, and Redis.
- Centralized logs and error monitoring.

## Release sequence

1. Run CI checks.
2. Build frontend and service images.
3. Apply reviewed database migrations.
4. Deploy backend and AI service.
5. Start or update workers.
6. Verify health endpoints and critical smoke tests.
7. Monitor logs and rollback if necessary.

Cloud deployment is planned and has not been executed in the current environment.

## Local production-like validation

Create a local `.env` from `.env.example`, replace the secret and service-token placeholders, then run:

```cmd
docker compose config
docker compose up --build
```

The backend container waits for healthy PostgreSQL and Redis services, applies migrations, and runs Gunicorn. The AI service exposes a readiness endpoint and accepts the shared `AI_SERVICE_TOKEN`. Cloud credentials, DNS, certificates, and managed-service provisioning remain environment-specific release steps.
