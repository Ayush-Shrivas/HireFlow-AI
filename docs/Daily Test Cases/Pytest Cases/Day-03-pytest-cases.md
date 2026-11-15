# Day 3 Pytest/API Test Cases

| Case | Expected result |
|---|---|
| Candidate submits to a published job | `201`, status is `APPLIED`, audit event is created |
| Candidate submits to the same job twice | Second request returns `400`; one application remains |
| Company recruiter transitions `APPLIED` to `REVIEWING` | `200`, history entry and audit event are created |
| Recruiter requests an invalid transition | `400`; status and history remain unchanged |
| Recruiter outside the job company reads an application | `404` due to object-level isolation |
| Recruiter outside the job company transitions an application | `403` |

Automated coverage is in `backend/apps/applications/tests/test_workflow.py` and passes with the complete backend suite.
