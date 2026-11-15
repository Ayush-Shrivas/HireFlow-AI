# ADR 001: Modular Monolith

## Decision

Use a Django modular monolith for core recruitment workflows.

## Rationale

The domain requires transactions across users, jobs, applications, and status history. A modular monolith reduces deployment and operational complexity while preserving clear domain boundaries.

## Consequence

Core Django apps share a database and deployment. Boundaries must be maintained through services, selectors, permissions, and tests.
