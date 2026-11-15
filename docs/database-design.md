# Database Design

## Database strategy

PostgreSQL is the production database. The schema is normalized around users, companies, jobs, applications, and workflow history. Foreign keys and unique constraints protect business invariants.

## Main entities

| Entity | Purpose | Important relationships |
|---|---|---|
| User | Identity and role | One candidate or recruiter profile |
| CandidateProfile | Candidate information | Skills, resumes, applications |
| RecruiterProfile | Recruiter information | Company memberships |
| Company | Employer organization | Recruiters and jobs |
| CompanyMembership | Recruiter-company relationship | Many-to-many bridge |
| Skill | Normalized skill catalog | CandidateSkill and JobSkill |
| Resume | Uploaded candidate document | One or more analyses |
| ResumeAnalysis | Structured extraction result | Belongs to Resume |
| Job | Published employment opportunity | Company, skills, applications |
| Application | Candidate submission | Candidate, job, history, interviews |
| ApplicationStatusHistory | Immutable workflow audit | Belongs to Application |
| SavedJob | Candidate bookmark | Candidate and Job |
| Interview | Scheduled hiring event | Belongs to Application |
| Notification | User-facing event | Belongs to User |
| Conversation | Candidate-recruiter thread | Messages |
| Message | Conversation content | Sender and Conversation |
| JobRecommendation | Ranked recommendation snapshot | Candidate and Job |
| AuditLog | Security and business audit trail | Actor and target object |

## Cardinality

```text
User 1--0..1 CandidateProfile
User 1--0..1 RecruiterProfile
Company 1--* Job
Company *--* RecruiterProfile through CompanyMembership
CandidateProfile *--* Skill through CandidateSkill
Job *--* Skill through JobSkill
CandidateProfile 1--* Application
Job 1--* Application
Application 1--* ApplicationStatusHistory
Application 1--* Interview
Conversation 1--* Message
```

## Constraints

- User email is unique.
- A candidate can submit only one application per job.
- A candidate can save a job only once.
- Job skills are unique per job and skill.
- Status history is append-only.
- Applications can only use valid state transitions.
- Resumes are private and owned by candidates.
- Recruiters can access applications only for their company jobs.

## Index plan

Index user email, job status/publication date, job company, application candidate/status, application job/status, notification recipient/read state, message conversation/timestamp, and normalized skill name.

Day 3 migrations implement `Application`, `ApplicationStatusHistory`, and `AuditEvent`. The `unique_candidate_job_application` constraint prevents duplicate submissions, while status history and audit records preserve workflow accountability.
