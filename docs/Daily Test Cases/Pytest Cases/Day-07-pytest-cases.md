# Day 7 Release Test Record

Backend system checks, migration checks, and the full Django suite are the release gate. AI-service health/readiness and analysis tests run with pytest. Frontend TypeScript and production build are checked in CI. Docker configuration includes service healthchecks; full container execution depends on Docker availability.
