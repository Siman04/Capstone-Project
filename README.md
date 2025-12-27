# Capstone-Project that involves building an application that tracks the expiry date of items like cosmetics, food, medicine e.t.c

## Week 1 — Setup & Planning (what's included here)

- Django project scaffold (`smartexpiry`)
- Apps created: `users`, `inventory`, `dashboard` (initial placeholders)
- Models added for `inventory` (Category, Item)
- User registration endpoint and JWT auth (via `djangorestframework-simplejwt`)
- `requirements.txt` with packages to install

## Quick setup (run locally)

1. Create a virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations and start the dev server:

```bash
python manage.py migrate
python manage.py runserver
```

## Running tests

Run the Django test suite:

```bash
python manage.py test
```

If you want to run tests for a specific app, include the app name:

```bash
python manage.py test inventory
python manage.py test dashboard
python manage.py test notifications
```


4. Endpoints available for Week 1:

- `POST /api/users/register/` — register a new user
- `POST /api/users/token/` — obtain JWT access & refresh tokens
- `POST /api/users/token/refresh/` — refresh JWT access token

## Week 2 — Inventory System (implemented)

Endpoints added:

- `GET /api/inventory/items/` — list authenticated user's items
- `POST /api/inventory/items/` — create item (accepts `category_id`)
- `GET /api/inventory/items/<id>/` — retrieve item details
- `PUT /api/inventory/items/<id>/` — update item
- `DELETE /api/inventory/items/<id>/` — delete item

- `GET /api/inventory/categories/` — list user's categories
- `POST /api/inventory/categories/` — create category
- `GET /api/inventory/categories/<id>/` — retrieve category
- `PUT /api/inventory/categories/<id>/` — update category
- `DELETE /api/inventory/categories/<id>/` — delete category

Notes:
- All inventory endpoints require authentication via JWT (use the tokens from `/api/users/token/`)
- When creating or updating an item you can pass `category_id` to associate an existing category that belongs to you.

## Notifications (Week 4)

- A management command `send_expiry_notifications` checks for items expiring in 3 days, 1 day, or today and emails the item's owner.
- For development the default email backend is the console backend. To send real emails, set `DJANGO_EMAIL_BACKEND` and `DJANGO_DEFAULT_FROM_EMAIL` environment variables (or configure Django settings accordingly).
- Example cron entry to run daily at 08:00:

```cron
# run at 08:00 daily
0 8 * * * /path/to/venv/bin/python /path/to/project/manage.py send_expiry_notifications
```

## CSV Export

- You can export your items as CSV at: `GET /api/inventory/items/export/` (must be authenticated).

---

## API Testing (Postman / Manual)

**Order of operations (important):**
- **Register first** using `POST /api/users/register/` with `{ "username": "<user>", "password": "<pass>" }`.
- **Then obtain a token** using `POST /api/users/token/` with the same credentials; use the returned **access** token in the `Authorization: Bearer <token>` header for protected endpoints.

**Common endpoints for testing**
- Register (POST): `/api/users/register/`  
  Body (JSON): `{ "username": "testuser", "password": "testpass" }`
- Obtain token (POST): `/api/users/token/`  
  Body (JSON): `{ "username": "testuser", "password": "testpass" }` returns `{ "access": "...", "refresh": "..." }`
- Create category (POST): `/api/inventory/categories/` — requires `Authorization: Bearer <access>`; body: `{ "name": "Food" }`  
- Create item (POST): `/api/inventory/items/` — requires `Authorization`; example body:

```json
{
  "name": "Milk",
  "category_id": 1,
  "quantity": 1,
  "purchase_date": "2025-12-27",
  "expiry_date": "2026-01-06",
  "notes": "Test"
}
```

**Notes & tips**
- If `register` returns `400` (user exists), skip straight to `token` with the existing credentials.
- In Postman, save the `access` token to an environment variable (e.g., `access_token`) after obtaining it, and set the `Authorization` header to `Bearer {{access_token}}` for subsequent requests.
- After creating a category, copy the `id` and store it as `category_id` to use when creating items.

**Public test URL (temporary tunnel)**
- If you need a public endpoint to test from outside this environment, a temporary tunnel URL may be provided (example: `https://swift-emus-dance.loca.lt`). The tunnel is temporary and may be restarted; if it is unavailable, start the dev server locally and/or create a new tunnel (ngrok/localtunnel).

---

## CI

- A GitHub Actions workflow is included at `.github/workflows/ci.yml` to run tests on push/PR to `main`.



Notes: Inventory API endpoints and dashboard will be implemented in Week 2 and beyond.
