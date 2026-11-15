# Troubleshooting

## `vite` is not recognized

Run `npm install` from `frontend`, then run `npm run dev`. Do not run npm commands from `backend`.

## `package.json` not found

The backend is Python/Django. Use `python manage.py runserver`.

## The terminal prompt still shows `C:\Users\Ayush>`

You are still on the C: drive. In Command Prompt, use:

```cmd
cd /d "E:\Final Project\HireFlow AI\frontend"
```

In PowerShell, use:

```powershell
Set-Location "E:\Final Project\HireFlow AI\frontend"
```

Confirm the prompt shows the expected project directory before running commands.

## Login fails

Confirm Django is running at port 8000, migrations have run, and the account was registered through `/register`.

## Docker command not found

Install and start Docker Desktop, or run PostgreSQL/Redis separately for local development.
