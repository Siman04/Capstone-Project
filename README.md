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

Notes: Inventory API endpoints and dashboard will be implemented in Week 2 and beyond.
