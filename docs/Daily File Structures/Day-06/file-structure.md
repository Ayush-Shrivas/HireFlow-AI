# Day 6 File Structure

Delivered changes:

- `backend/apps/interviews/`: interview model, API, notifications, migration, and tests.
- `backend/apps/notifications/`: recipient-scoped notifications and read API.
- `backend/apps/messaging/`: conversations, messages, read state, REST API, and WebSocket consumer.
- `backend/apps/analytics/`: role-scoped dashboard metrics endpoint.
- `backend/config/routing.py` and `backend/config/asgi.py`: optional authenticated Channels routing.

Expected changes: interview and notification models, Channels consumers, messaging models, analytics selectors, dashboard components, and real-time tests.
