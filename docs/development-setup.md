# Development Setup

## Prerequisites

- Python 3.12+.
- Node.js 20+ and npm.
- PostgreSQL and Redis are optional for Day 1. Docker is not required.

## Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements\development.txt
python manage.py migrate
python manage.py runserver
```

Backend health: `http://127.0.0.1:8000/health/`

## AI service

```powershell
cd ai-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

AI health: `http://127.0.0.1:8001/health`

## Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173/`

Frontend verification:

```powershell
cd frontend
npm ci
npm test
npm run build
npx playwright install chromium
npm run test:e2e
```

## Environment

Copy `.env.example` to `.env`. Never commit `.env` or real secrets.

## Local development without Docker

When PostgreSQL is unavailable, development settings use SQLite for Day 1 local development and isolated tests. Redis is not required until Celery, caching, or WebSockets are implemented. Production configuration will require PostgreSQL and Redis.

## Optional Docker workflow

Docker Compose is retained for future team and deployment environments, but is not part of the required local workflow.
