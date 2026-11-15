# Security Architecture

## Security principles

Security is enforced server-side. Frontend role state is only presentation state and is never trusted for authorization.

## Controls

- Django password hashing and password validators.
- JWT expiration, rotation, and blacklisting.
- CORS allowlist from environment configuration.
- CSRF protection for cookie-authenticated browser flows.
- ORM queries to avoid SQL injection.
- Serializer validation for all external input.
- Object-level permissions for users, companies, jobs, applications, resumes, and conversations.
- Private resume storage with generated filenames.
- Upload size, extension, MIME, and parser limits.
- Rate limiting on authentication, uploads, and AI endpoints.
- Secure headers and HTTPS in production.
- Append-only audit logging for sensitive actions.

## Sensitive data policy

Never log passwords, access tokens, refresh tokens, API keys, resume contents, private messages, or unnecessary personal information.

## AI safety

AI scores assist recruiters and do not automatically reject candidates. Matching uses job-relevant qualifications and must exclude protected or unrelated personal characteristics. AI output is validated and stored with processing status and confidence metadata where applicable.

## Threats to test

IDOR, privilege escalation, token reuse, brute-force login, malicious files, path traversal, WebSocket authorization bypass, excessive API access, XSS, CSRF, and sensitive response leakage.
