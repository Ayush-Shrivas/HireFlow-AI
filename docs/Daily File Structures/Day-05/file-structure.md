# Day 5 File Structure

Delivered changes:

- `backend/apps/recommendations/models.py`: persisted `MatchResult` records.
- `backend/apps/recommendations/services.py`: deterministic scoring and recommendation selectors.
- `backend/apps/recommendations/serializers.py`: explainable match response.
- `backend/apps/recommendations/views.py` and `urls.py`: protected recommendation APIs.
- `backend/apps/recommendations/migrations/0001_initial.py`: match-result schema and uniqueness constraint.
- `backend/apps/recommendations/tests/test_matching.py`: Day 5 workflow tests.

Expected changes: matching and recommendation services, result models, AI schemas, scoring tests, recommendation API, and candidate/recruiter UI.
