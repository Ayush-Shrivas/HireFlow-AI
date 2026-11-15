# Starting Services

Start the services without Docker in three terminals.

For Windows Command Prompt (`cmd.exe`), use `cd /d` so the command changes both the drive and directory:

```powershell
cd /d "E:\Final Project\HireFlow AI\backend"
python manage.py runserver
```

```powershell
cd /d "E:\Final Project\HireFlow AI\ai-service"
uvicorn app.main:app --reload --port 8001
```

```powershell
cd /d "E:\Final Project\HireFlow AI\frontend"
npm run dev
```

The optional Docker workflow is:

```powershell
docker compose up --build
```

Expected endpoints:

- Backend: `http://localhost:8000/health/`
- AI service: `http://localhost:8001/health`
- Frontend: `http://localhost:5173/`
