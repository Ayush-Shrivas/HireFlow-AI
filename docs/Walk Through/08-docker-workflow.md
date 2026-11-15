# Optional Docker Workflow

Docker is not required for local Day 1 development.

If Docker is used later, copy `.env.example` to `.env`, then run:

```powershell
docker compose up --build
```

Stop services with `docker compose down`. Add `-v` only when intentionally removing local database volumes.
