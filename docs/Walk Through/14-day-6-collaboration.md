# Day 6 Collaboration Walkthrough

## Schedule an interview

```powershell
curl.exe -X POST http://localhost:8000/api/v1/interviews/ -H "Authorization: Bearer RECRUITER_ACCESS_TOKEN" -H "Content-Type: application/json" -d "{\"application\":1,\"start_at\":\"2026-10-21T10:00:00Z\",\"end_at\":\"2026-10-21T11:00:00Z\",\"meeting_url\":\"https://meet.example.com/room\"}"
```

The candidate receives a private interview notification.

## Send a message

Create a conversation with participant ids, then use `/api/v1/conversations/{id}/messages/`. Every message is restricted to conversation participants and creates a recipient notification. PATCH the message read endpoint to record read state.

For real-time delivery, connect to `ws://localhost:8000/ws/conversations/{id}/?token=ACCESS_TOKEN`. The Channels consumer validates the JWT and conversation membership before accepting the socket.

## Dashboard metrics

Request `/api/v1/analytics/dashboard/` with a candidate or recruiter JWT. Candidates receive their application/interview counts; recruiters receive counts limited to their company memberships.

## Verification

Run `python manage.py test apps.interviews.tests.test_day6 -v 1` from `backend`.
