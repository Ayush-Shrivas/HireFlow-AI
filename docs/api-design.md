# API Design

## Conventions

Base path: `/api/v1/`

- JSON request and response bodies.
- JWT access authentication for protected endpoints.
- Pagination for collections.
- Explicit serializer validation.
- Object-level authorization in Django.
- Consistent error objects.

## Day 1 endpoints

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| POST | `/auth/register/` | Public | Create candidate or recruiter |
| POST | `/auth/login/` | Public | Issue access and refresh tokens |
| POST | `/auth/refresh/` | Public | Refresh access token |
| POST | `/auth/logout/` | Authenticated | Blacklist refresh token |
| GET | `/auth/me/` | Authenticated | Return current user |
| GET | `/health/` | Public | Backend health |

## Day 2 domain endpoints

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET/PATCH | `/candidates/profile/` | Candidate | Read or update the current candidate profile |
| GET/PATCH | `/recruiters/profile/` | Recruiter | Read or update the current recruiter profile |
| GET/POST | `/companies/` | Authenticated | List memberships or create a company |
| GET/PATCH/DELETE | `/companies/{id}/` | Company member | Manage a member company |
| GET/POST | `/companies/{id}/members/` | Owner for POST | List or add company members |
| GET/POST | `/jobs/skills/` | Authenticated | Search or create normalized skills |
| GET/POST | `/jobs/` | Authenticated | Browse published jobs or create a member-owned draft |
| GET/PATCH/DELETE | `/jobs/{id}/` | Member | Manage a company job |
| POST | `/jobs/{id}/publish/` | Member | Publish a draft job |
| POST | `/jobs/{id}/close/` | Member | Close a job |

### Day 2 job query parameters

`search` searches title, description, location, company, and skill name. `location`, `employment_type`, and `min_experience` provide additional filters. `ordering` supports `created_at`, `title`, `min_experience`, and `salary_min`; prefix with `-` for descending order. Collections use page-number pagination with a default page size of 10.

```text
/candidates/me/
/companies/
/jobs/
/jobs/{id}/publish/
/jobs/{id}/apply/
/applications/
/applications/{id}/status/
/applications/{id}/interviews/
/notifications/
/conversations/
/recommendations/
```

## Error format

```json
{
  "error": {
    "code": "INVALID_STATUS_TRANSITION",
    "message": "The requested application transition is not allowed.",
    "details": {}
  }
}
```

Do not return stack traces, secrets, tokens, file paths, or internal database details.

## Day 3 application endpoints

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET/POST | `/applications/` | Candidate for POST | List visible applications or submit a published-job application |
| GET | `/applications/{id}/` | Candidate, company recruiter, or admin | View an application within the caller's scope |
| POST | `/applications/{id}/transition/` | Company recruiter or admin | Move an application through an allowed hiring status |

Applications expose `candidate_email`, `job_title`, `company_name`, `status`, and immutable `history` entries. Valid transitions are `APPLIED → REVIEWING → SHORTLISTED → INTERVIEW → OFFERED → HIRED`; rejection is allowed from each active review stage. Terminal `HIRED` and `REJECTED` applications cannot transition further.

## Day 4 resume endpoints

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET/POST | `/resumes/` | Candidate | List private resumes or upload a new resume |
| GET | `/resumes/{id}/` | Owner candidate | View processing status, extracted text, and analysis |

Uploads accept PDF, DOC, DOCX, and TXT files up to the configured size limit. Processing is asynchronous when Celery is available and synchronous in the local test fallback. Statuses are `UPLOADED`, `PROCESSING`, `READY`, and `FAILED`.

## Day 5 recommendation endpoints

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `/recommendations/` | Candidate | Return ranked recommendations for eligible published jobs |
| GET | `/recommendations/{job_id}/` | Candidate | Return a persisted explainable match for one eligible job |

Match scores are bounded from 0–100: skills contribute 60 points, experience contributes 20, and semantic text overlap contributes 20. Responses include score components, matched skills, missing skills, weighting, and explanation. Applied and closed jobs are excluded.

## Google authentication endpoints

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `/auth/google/login/` | Public | Redirect to Google consent |
| GET | `/auth/google/callback/` | Public | Verify Google identity and redirect with HireFlow JWTs |

Google sign-in is disabled safely with HTTP 503 until `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are configured. OAuth state is stored in the Django session to prevent callback forgery.

## Day 6 collaboration endpoints

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET/POST | `/interviews/` | Scoped user/recruiter | List or schedule interviews |
| GET/PATCH | `/interviews/{id}/` | Scoped user | View or update an interview |
| GET | `/notifications/` | Recipient | List private notifications |
| PATCH | `/notifications/{id}/read/` | Recipient | Mark a notification read |
| GET/POST | `/conversations/` | Participant | List or create conversations |
| GET/POST | `/conversations/{id}/messages/` | Participant | Read or send messages |
| PATCH | `/conversations/messages/{id}/read/` | Participant | Mark a message read |
| GET | `/analytics/dashboard/` | Candidate/recruiter | Return role-scoped dashboard metrics |

Authenticated real-time messages use `ws://localhost:8000/ws/conversations/{id}/?token=ACCESS_TOKEN`. The connection is rejected unless the JWT is valid and the user participates in the conversation.
