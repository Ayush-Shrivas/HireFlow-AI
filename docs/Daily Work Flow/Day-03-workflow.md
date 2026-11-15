# Day 3 Workflow

Implement applications and the controlled hiring workflow. Add a database uniqueness constraint, transition service, status history, applicant views, and audit events. Verify duplicate applications, valid transitions, invalid transitions, and role isolation.

## Completion record

Day 3 is complete at 100% for the planned application workflow scope.

- Application and status-history models are migrated.
- Candidate applications are unique per job and duplicate submissions return a clear error.
- Recruiters can view applications for their company and use controlled status transitions.
- Candidates can submit applications and track status history.
- Audit events are recorded for application creation and status changes.
- Role isolation, duplicate applications, valid transitions, and invalid transitions are covered by the Day 3 workflow tests.
- Backend tests, migration checks, frontend TypeScript checks, and the production build pass.
