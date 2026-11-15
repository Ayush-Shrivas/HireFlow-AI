# Day 1 CLI Test Cases

| Command | Purpose | Result |
|---|---|---|
| `python manage.py makemigrations accounts` | Generate account migration | PASS |
| `python manage.py migrate --noinput` | Apply database migrations | PASS |
| `python manage.py test apps.accounts.tests -v 1` | Run authentication tests | PASS: 6 tests |
| `python -m pytest -q` in `ai-service` | Run AI service tests | PASS: 1 test |
| `npm run build` in `frontend` | Build frontend | PASS |
| `npm test` in `frontend` | Run authentication component tests | PASS: 3 tests |
| `docker compose config` | Validate optional Docker YAML | PASS: YAML valid |

The AI test was executed with `-p no:cacheprovider` because the environment generated inaccessible pytest cache directories. The test itself passed.
