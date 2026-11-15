# ADR 003: Application Status Workflow

## Decision

Applications use explicit states: `APPLIED`, `SCREENING`, `SHORTLISTED`, `INTERVIEW`, `OFFER`, `HIRED`, and terminal `REJECTED`.

## Rationale

Explicit transitions prevent inconsistent hiring data and make reporting, notifications, and audit history reliable.

## Consequence

All changes go through a transition service. Every valid change creates an immutable status-history record and an audit event.
