# AI Architecture

## Scope

The FastAPI service will process resumes and calculate explainable job matches. It does not own users, jobs, or applications.

## Planned pipeline

```text
Private resume upload
  -> Django validation
  -> Celery task
  -> FastAPI extraction
  -> Structured parsing
  -> Skill normalization
  -> Match/recommendation calculation
  -> Django persistence
  -> Candidate/recruiter notification
```

## Matching model

The initial deterministic score is:

```text
45% required/preferred skill match
25% relevant experience
20% semantic similarity
10% education or preference match
```

Every score must expose component values, matched skills, missing skills, and a human-readable explanation. Scores are bounded from 0 to 100 and must be covered by unit tests.

## Resume failure states

`PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`, and `UNSUPPORTED` are persisted so failures are visible and retryable.

## Quality and safety

Extraction is probabilistic. Structured output is validated before persistence. Scanned or empty documents are reported clearly. The platform must not use protected characteristics for ranking or automatic rejection.
