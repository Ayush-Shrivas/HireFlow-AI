# Day 6 Workflow

## Scope

Interview scheduling, notifications, protected conversations, message read state, authenticated Channels messaging, and dashboard metrics.

## Delivered

- Recruiters can schedule and update interviews for applications within their company; candidates can view their own interviews.
- Scheduling and messaging create recipient-scoped notifications.
- Conversations require authenticated participants; messages are protected by conversation membership.
- Messages support REST delivery, read timestamps, and an authenticated WebSocket consumer at `ws/conversations/{id}/?token=ACCESS_TOKEN`.
- Candidate and recruiter dashboard metrics are scoped to their own applications, companies, interviews, jobs, and unread conversations.
- Tests cover scheduling, access isolation, notification delivery, messaging, read state, and dashboard metrics.

## Completion

Day 6 is complete at 100% for the planned collaboration and analytics scope. Browser automation is documented as not installed; API and model tests are the verification authority.
