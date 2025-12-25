# Cyethack Threat Monitoring Backend

**Overview**
- **Project**: Cyethack Threat Monitoring API — a small Django + DRF backend to ingest security events and generate alerts.
- **Apps**: `threats`, `users`
- **Main router**: [config/config/urls.py](config/config/urls.py#L1-L200)

**Requirements**
- Python 3.10+ (recommended)
- SQLite (default, configured in `config/config/settings.py`)
- Python packages (install via pip):
  - Django
  - djangorestframework
  - djangorestframework-simplejwt
  - django-filter
  - drf-yasg

Quick install (example)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install django djangorestframework djangorestframework-simplejwt django-filter drf-yasg
```

Run locally
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Database**
- Uses SQLite by default at `db.sqlite3` (see [config/config/settings.py](config/config/settings.py#L1-L200)).

**Models (summary)**
- `Event` (`threats/models.py`):
  - `source_name` (string)
  - `event_type` (string)
  - `severity` (LOW|MEDIUM|HIGH|CRITICAL)
  - `description` (text)
  - `timestamp` (auto, read-only)
- `Alert` (`threats/models.py`):
  - `event` (OneToOne -> `Event`)
  - `status` (OPEN|ACK|RESOLVED)
  - `created_at` (auto, read-only)

See model definitions: [config/threats/models.py](config/threats/models.py#L1-L200).

**Serializers**
- `EventSerializer`: All fields, `timestamp` read-only. See [config/threats/serializers.py](config/threats/serializers.py#L1-L120).
- `AlertSerializer`: nests `Event` as read-only, `created_at` read-only.

**Authentication & Permissions**
- JWT (Simple JWT) is used. Endpoints for tokens are exposed in the root URLs.
- Default DRF permission class is `IsAuthenticated` (see settings).
- `AlertViewSet` restricts `update`/`partial_update` to admin users.

API docs (Swagger / Redoc)
- Swagger UI: `GET /swagger/`
- Redoc: `GET /redoc/`

API Endpoints
- Admin: `GET/POST` at `/admin/`

- JWT Token endpoints (see [config/config/urls.py](config/config/urls.py#L1-L80)):
  - `POST /api/token/` — Obtain access & refresh tokens. Body: `{"username": "...", "password": "..."}`
  - `POST /api/token/refresh/` — Refresh access token. Body: `{"refresh": "<refresh_token>"}`

- Events (ViewSet registered as `events`)
  - `GET /api/events/` — List events (paginated, default page size 10)
  - `POST /api/events/` — Create event. Body JSON (example):
    ```json
    {
      "source_name": "sensor-1",
      "event_type": "login_failure",
      "severity": "HIGH",
      "description": "Multiple failed logins from IP x.x.x.x"
    }
    ```
    - `timestamp` is set automatically and returned in response.
    - When an `Event` with `severity` `HIGH` or `CRITICAL` is created, an `Alert` is automatically created by the viewset (`threats/views.py`).
  - `GET /api/events/{id}/` — Retrieve event
  - `PUT/PATCH /api/events/{id}/` — Update event
  - `DELETE /api/events/{id}/` — Delete event

- Alerts (ViewSet registered as `alerts`)
  - `GET /api/alerts/` — List alerts
    - Supports filtering with query params: `?status=OPEN` and `?event__severity=HIGH` (see `filterset_fields` in `AlertViewSet`).
  - `GET /api/alerts/{id}/` — Retrieve alert (includes nested `event` data)
  - `POST /api/alerts/` — Not intended for normal use. Note: `AlertSerializer` declares `event` as read-only; alerts are normally created automatically when high-severity events are ingested.
  - `PUT/PATCH /api/alerts/{id}/` — Update alert (only admin users may update/partial_update)
  - `DELETE /api/alerts/{id}/` — Delete alert

Authentication header example
```http
Authorization: Bearer <access_token>
```

Example cURL flows
- Obtain token:
```bash
curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d '{"username":"admin","password":"pass"}'
```

- Create an event (using obtained token):
```bash
curl -X POST http://127.0.0.1:8000/api/events/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"source_name":"sensor-1","event_type":"scan","severity":"CRITICAL","description":"Port scan detected"}'
```

Notes, caveats & behavior
- Alerts are generated automatically for `HIGH` and `CRITICAL` events by `EventViewSet.perform_create` (see [config/threats/views.py](config/threats/views.py#L1-L120)).
- `AlertSerializer` nests `Event` as read-only; creating alerts through the API may not accept `event` as a writable field. Prefer creating `Event` objects to trigger alerts.
- Pagination: Page size is configured via `REST_FRAMEWORK.PAGE_SIZE` (default 10).
- Rate limiting: `UserRateThrottle` set to `100/day` for users.

Where to look next
- URL routing and registry: [config/config/urls.py](config/config/urls.py#L1-L120)
- Threats app (models, serializers, views): [config/threats](config/threats)
- Settings and JWT config: [config/config/settings.py](config/config/settings.py#L1-L200)

Want me to:
- add a `requirements.txt` and pin versions? (yes/no)
- expand the README with full OpenAPI examples or Postman collection? (yes/no)
