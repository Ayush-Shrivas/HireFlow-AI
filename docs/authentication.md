# Authentication Architecture

## Current design

Authentication is email-based JWT authentication implemented by Django REST Framework SimpleJWT.

- Access tokens are short-lived.
- Refresh tokens last longer and are rotated.
- Rotated refresh tokens are blacklisted.
- Passwords are hashed by Django.
- Public registration supports candidates and recruiters.
- Administrator accounts are not created through public registration.
- `/api/v1/auth/me/` is protected.

## Browser behavior

The frontend stores the Day 1 token state locally for the prototype flow. Before production, refresh tokens should use Secure, HttpOnly, SameSite cookies and access tokens should be held in memory where practical.

## Password and login policy

Passwords must be at least eight characters and pass Django validators. Login failures should not reveal whether an email exists. Rate limiting will be added before production.

## Planned improvements

- Password reset.
- Email verification.
- Login throttling.
- Device/session management.
- Production cookie-based refresh flow.
- Audit events for login, logout, and password changes.

## Google sign-in

The login screen’s `Continue with Google` button starts an OAuth 2.0 authorization-code flow at `/api/v1/auth/google/login/`. Django validates the returned Google ID token, creates or finds a candidate account by verified email, and redirects to the frontend callback with the project’s normal access and refresh JWTs.

Configure these environment variables before enabling the button:

```text
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback/
FRONTEND_URL=http://localhost:5173
```

The Google Cloud OAuth client must allow the exact redirect URI above. New Google accounts are created as candidates; existing accounts retain their current role.
