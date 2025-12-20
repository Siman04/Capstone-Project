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

## CI

- A GitHub Actions workflow is included at `.github/workflows/ci.yml` to run tests on push/PR to `main`.



Notes: Inventory API endpoints and dashboard will be implemented in Week 2 and beyond.
