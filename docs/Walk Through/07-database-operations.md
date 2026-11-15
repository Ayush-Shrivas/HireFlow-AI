# Database Operations

```powershell
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
```

Production migrations must be reviewed before deployment. Never delete production data to resolve a migration problem.
