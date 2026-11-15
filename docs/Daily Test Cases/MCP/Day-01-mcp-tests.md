# Day 1 MCP Test Cases

MCP/desktop verification checklist:

1. Open the frontend at `http://localhost:5173/`.
2. Confirm the login page renders.
3. Navigate to registration.
4. Register a candidate account.
5. Return to login and authenticate.
6. Confirm the dashboard displays the authenticated email.
7. Log out and confirm the protected dashboard redirects to login.

Status: the frontend rendered successfully at `http://localhost:5173/`. Registration/login interaction requires Django to be running. Docker is not required.
