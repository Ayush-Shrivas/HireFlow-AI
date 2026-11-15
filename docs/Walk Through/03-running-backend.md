# Running the Backend

```powershell
cd "E:\Final Project\HireFlow AI\backend"
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/health/`. Run authentication tests with `python manage.py test apps.accounts.tests -v 1`.
