# ADR 002: Separate AI Service

## Decision

Run AI processing in a separate FastAPI service.

## Rationale

AI dependencies, processing time, model lifecycle, and scaling needs differ from transactional recruitment APIs.

## Consequence

Django remains the business-data authority. Communication requires authenticated internal requests and validated schemas. Network failure and AI failure must be represented as retryable processing states.
