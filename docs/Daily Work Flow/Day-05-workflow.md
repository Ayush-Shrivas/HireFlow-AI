# Day 5 Workflow

## Scope

Deterministic explainable matching, semantic text overlap, missing skills, skill-gap recommendations, stored match results, and ranked job recommendations.

## Delivered

- Match results persist per candidate/job with a uniqueness constraint.
- Scores are bounded from 0–100 using skills (60%), experience (20%), and semantic similarity (20%).
- Results expose matched skills, missing skills, score components, weights, and a human-readable explanation.
- Recommendations include published jobs only and exclude closed jobs and jobs already applied to by the candidate.
- Candidate-only list/detail endpoints are protected from recruiter access.
- Tests cover score ordering, score bounds, missing skills, applied/closed-job exclusion, persistence, and role isolation.

## Completion

Day 5 is complete at 100% for the planned matching and recommendation scope. Browser automation is documented as not installed; API tests are the verification authority.
