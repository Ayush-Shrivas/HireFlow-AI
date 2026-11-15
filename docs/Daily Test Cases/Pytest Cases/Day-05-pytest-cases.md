# Day 5 Pytest/API Test Cases

Automated coverage is in `backend/apps/recommendations/tests/test_matching.py`.

| Case | Expected result |
|---|---|
| Candidate requests recommendations | Ranked persisted results are returned |
| Matching score | Score remains between 0 and 100 |
| Matching explanation | Components, weights, matched skills, and missing skills are present |
| Applied job | Excluded from recommendations |
| Closed job | Excluded from recommendations |
| Recruiter access | HTTP 403 |

Command: `python manage.py test apps.recommendations.tests.test_matching -v 1`.
