# Day 5 Matching and Recommendations Walkthrough

## Generate recommendations

Authenticate as a candidate and request:

```powershell
curl.exe http://localhost:8000/api/v1/recommendations/ -H "Authorization: Bearer ACCESS_TOKEN"
```

The response is ranked by score and includes the job, company, total score, component scores, matched skills, missing skills, and explanation.

## Match calculation

The service reads the candidate's latest ready resume analysis and profile experience. It compares those skills with the job's normalized skills and calculates deterministic text overlap between the resume and job text. Scores use 60% skills, 20% experience, and 20% semantic similarity.

## Eligibility rules

Only published jobs are considered. Closed jobs and jobs with an existing candidate application are excluded. Recruiters cannot access candidate recommendation results.

## Verification

Run `python manage.py test apps.recommendations.tests.test_matching -v 1` from `backend`.
