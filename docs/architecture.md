# HireFlow AI System Architecture

## Status

This document describes the target architecture. Days 1–4 currently implement the repository foundation, Django authentication, marketplace and application workflows, private resume processing, FastAPI health/analysis endpoints, and the initial React authentication screens.

## Architectural style

HireFlow AI uses a modular monolith for core business capabilities and a separate FastAPI service for AI workloads.

```text
React/TypeScript frontend
          |
       HTTPS
          v
Django REST Framework ---- PostgreSQL
          |
          +---- Redis / Celery / Channels
          |
          +---- FastAPI AI service
```

## Service responsibilities

| Service | Responsibility | Data authority |
|---|---|---|
| Frontend | User interface and client-side state | None |
| Django | Users, permissions, jobs, applications, interviews, notifications | Primary business data |
| FastAPI | Resume extraction, matching, recommendations | No business records |
| PostgreSQL | Durable relational data | System of record |
| Redis | Cache, broker, channel layer, temporary state | None |
| Celery | Asynchronous and retryable work | Task status only |

## Domain boundaries

Django applications are separated by business domain: `accounts`, `candidates`, `recruiters`, `companies`, `jobs`, `applications`, `interviews`, `notifications`, `messaging`, `analytics`, `audit`, and `ai_integration`.

Views handle HTTP concerns. Services handle business operations and transactions. Selectors handle reusable read queries. Tasks handle asynchronous work.

## Core request flow

1. The frontend sends an authenticated REST request.
2. Django authenticates the token and checks object-level permissions.
3. A domain service validates business rules and writes a transaction.
4. Django returns a safe serialized response.
5. Long-running work is submitted to Celery.
6. The frontend receives updates through REST or WebSockets.

## Current implementation boundary

Implemented on Days 1–4: PostgreSQL-compatible settings, local SQLite test fallback, Redis/Celery configuration, JWT authentication, candidate/recruiter registration, marketplace and application workflows, private resume upload validation, retryable processing, text extraction, FastAPI resume analysis, protected APIs, and minimal React login/registration flows.

Planned: matching, recommendations, Channels consumers, messaging, analytics, and production deployment.
