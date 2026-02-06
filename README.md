# Gradus Notifications — Setup & API Guide

This project provides:
- Admin-only APIs to manage notification types and templates.
- Validation for template HTML, Django template syntax, and required variables.
- A notification service with channel abstractions and an email implementation.
- An API endpoint to send notifications via the service.

## Requirements Covered (per task)
- API to add new notification types (superuser only).
- API to create/update/delete notification templates with validation.
- Notification sending interface with specific methods for each type.
- Channel abstraction + email channel implementation.

## Quick Start (Docker + Makefile)

1) Configure environment:
   - Update `.env` with your SMTP credentials (see the example below).

2) Build and start containers:
```
make build
make start
```

3) Run migrations and create a superuser:
```
docker exec -it app bash
python src/manage.py migrate
python src/manage.py createsuperuser
```

4) Stop containers:
```
make stop
```

## Environment Configuration (SMTP)
Example for Gmail (use an App Password):
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=app_password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=your@gmail.com
```

Note: `EmailChannel` sends to `user.email`. Make sure the user has an email set.

## API Endpoints (Admin Only)

Base path: `http://localhost:8000/api/notifications/`

### Notification Types
- `GET /types/` — list types
- `POST /types/` — create a new type

Payload example:
```
{
  "code": "password_recovery",
  "name": "Password recovery",
  "allowed_channels": ["email"],
  "allowed_variables": ["recovery_token"],
  "is_singleton_template": true
}
```

### Notification Templates
- `GET /templates/` — list templates
- `POST /templates/` — create template
- `PATCH /templates/{id}/` — update template
- `DELETE /templates/{id}/` — delete template (only for `custom`)

Payload example (confirm_email):
```
{
  "type": 2,
  "name": "",
  "title": "Confirm email",
  "html": "Token: {{ confirmation_token }}"
}
```

Payload example (new_survey — must be plain text because push is allowed):
```
{
  "type": 1,
  "name": "",
  "title": "",
  "html": "New survey: {{ title }}"
}
```

### Send Notification
- `POST /send/`

Payload example:
```
{
  "type_code": "confirm_email",
  "user_id": 1,
  "context": { "confirmation_token": "TEST123" },
  "channels": ["email"]
}
```

Payload example for `custom`:
```
{
  "type_code": "custom",
  "template_name": "promo_1",
  "user_id": 1,
  "context": { "title": "Hello" },
  "channels": ["email"]
}
```

## Template Validation Rules

- **Allowed HTML tags**
  - `email`: `p`, `b`, `i`, `a`, `br`
  - `telegram`, `viber`: `p`, `br`
  - `push`: no HTML tags allowed
- **Title**
  - Must be empty if `telegram` or `viber` is in allowed channels.
- **Variables**
  - All variables listed in the notification type must appear in `html`.
  - No extra variables are allowed.
  - Example: `{{ confirmation_token }}` or `{% if confirmation_token %}...{% endif %}`.

## Test Script (API Requests)

A helper script is provided to test endpoints via `requests`:
```
python api_requests_check.py
```

Environment variables:
- `API_BASE_URL` (default: `http://localhost:8000`)
- `API_USERNAME` / `API_PASSWORD`
- `SHOW_FULL=true` for full stdout output
- `API_CHECK_LOG=api_requests_check.log`
