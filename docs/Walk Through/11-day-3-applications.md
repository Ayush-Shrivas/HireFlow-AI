# Day 3 Applications Walkthrough

1. Start the backend and obtain a candidate access token through the existing login flow.
2. Browse published jobs with `GET /api/v1/jobs/`.
3. Submit an application with `POST /api/v1/applications/` and `{ "job": <published-job-id>, "cover_note": "..." }`.
4. Confirm the candidate sees the application in `GET /api/v1/applications/` and in the dashboard tracking panel.
5. Log in as a recruiter who belongs to the job's company.
6. Confirm the application appears in the recruiter pipeline.
7. Move it through the controlled status selector. Each successful transition creates a status-history entry and audit event.
8. Confirm duplicate submissions return `400`, invalid transitions return `400`, and users outside the company cannot view or transition the application.
