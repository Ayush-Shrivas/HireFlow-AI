# Day 4 Resume Processing Walkthrough

## Upload a resume

Authenticate as a candidate, then send a multipart request:

```powershell
curl.exe -X POST http://localhost:8000/api/v1/resumes/ -H "Authorization: Bearer ACCESS_TOKEN" -F "file=@resume.txt;type=text/plain"
```

The response includes the resume id and its current processing status. Poll `/api/v1/resumes/{id}/` to observe `PROCESSING`, `READY`, or `FAILED`.

## Processing behavior

TXT files are extracted locally. The backend sends extracted text to `AI_SERVICE_URL/v1/resumes/analyze`; if the service is unavailable, a safe pending analysis is stored. Celery retries failed tasks twice when a broker is available.

## Security behavior

Only the candidate who uploaded a resume can list or retrieve it. Empty files, files over 5 MB by default, unsupported extensions, and executable content types are rejected before storage.

## Verification

Run `python manage.py test apps.candidates.tests.test_resumes -v 1` from `backend`.
