# Running Tests

Backend:

```powershell
cd backend
python manage.py check
python manage.py test apps.accounts.tests -v 1
```

AI service:

```powershell
cd ai-service
python -m pytest -q
```

Frontend and Playwright commands will be enabled after their dependencies are installed.
