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


Notes: Inventory API endpoints and dashboard will be implemented in Week 2 and beyond.
