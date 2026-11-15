# Running the AI Service

```powershell
cd "E:\Final Project\HireFlow AI\ai-service"
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Open `http://localhost:8001/health`. Resume and matching endpoints are planned after Day 1.
