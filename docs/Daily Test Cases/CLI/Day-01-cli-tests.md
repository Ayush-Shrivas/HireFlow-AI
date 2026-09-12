# Day 1 CLI Test Cases

| Command | Purpose | Result |
|---|---|---|
| `python manage.py makemigrations accounts` | Generate account migration | PASS |
| `python manage.py migrate --noinput` | Apply database migrations | PASS |
| `python manage.py test apps.accounts.tests -v 1` | Run authentication tests | PASS: 4 tests |
| `python -m pytest -q` in `ai-service` | Run AI service tests | PASS: 1 test |
| `npm run build` in `frontend` | Build frontend | BLOCKED: dependencies unavailable |
