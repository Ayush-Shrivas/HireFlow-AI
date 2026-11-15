# Day 2 CLI Test Cases

| Command | Result |
|---|---|
| `python manage.py makemigrations candidates recruiters companies jobs` | PASS |
| `python manage.py migrate --noinput` | PASS |
| `python manage.py check` | PASS |
| `python manage.py test apps.accounts.tests apps.jobs.tests -v 1` | PASS: 11 tests |
| `npm test` in `frontend` | PASS: 3 tests |
| `npm run build` in `frontend` | PASS |
