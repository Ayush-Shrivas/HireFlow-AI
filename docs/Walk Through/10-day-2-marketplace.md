# Day 2 Marketplace Walkthrough

## Start the services

From Command Prompt:

```cmd
cd /d "E:\Final Project\HireFlow AI\backend"
python manage.py migrate
python manage.py runserver
```

In a second terminal:

```cmd
cd /d "E:\Final Project\HireFlow AI\frontend"
npm run dev
```

Open `http://localhost:5173/`.

## Candidate flow

Register as a candidate, sign in, and open the dashboard. The marketplace requests `GET /api/v1/jobs/` and displays published jobs. Use the search field to send the `search` query parameter. Candidate profile data is managed at `GET/PATCH /api/v1/candidates/profile/`.

## Recruiter flow

Register as a recruiter, then create a company with `POST /api/v1/companies/`. The creator automatically receives an `OWNER` membership. Create a draft job with `POST /api/v1/jobs/`, including the company ID and optional skill IDs. Publish it with `POST /api/v1/jobs/{id}/publish/`.

## Permission rules

- Only authenticated users can access Day 2 endpoints.
- Candidate accounts manage candidate profiles; recruiter accounts manage recruiter profiles.
- A recruiter must be a member of a company to create or manage its jobs.
- Only company owners can add memberships.
- Candidates can see published jobs; company members can also see and manage their drafts.

## Troubleshooting

If the marketplace is empty, confirm that a recruiter has created and published a job. If the frontend cannot reach the API, confirm Django is running on `http://localhost:8000` and that the frontend uses the default API base URL.
