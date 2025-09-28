# Restaurant Finder

A Django-based web application for searching nearby restaurants with live map data. This repository contains the foundational project structure configured for deployment on Heroku with a Postgres database.

## Features (Planned)
- Map-based search experience with live data refreshes
- Postgres-backed persistence for restaurant details and user activity
- Ready-to-deploy configuration for Heroku buildpacks

## Project Structure
```
.
├── Procfile
├── README.md
├── manage.py
├── requirements.txt
├── restaurant_finder
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── restaurants
│   ├── __init__.py
│   ├── apps.py
│   ├── templates
│   │   └── restaurants
│   │       └── home.html
│   ├── static
│   │   └── restaurants
│   │       └── css
│   │           └── base.css
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   └── tests.py
├── runtime.txt
└── .gitignore
```

## Getting Started

### Prerequisites
- Python 3.11+
- pip
- (Optional) Virtual environment tooling such as `venv` or `pipenv`

### Local Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` to confirm the starter page renders.

### Environment Variables
Create a `.env` file (or set environment variables in your shell) with at least:
```
DJANGO_SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DB_NAME
```

### Running Tests
```bash
python manage.py test
```

## Deployment
1. Provision a Postgres database on Heroku and copy the connection string to `DATABASE_URL`.
2. Add the Heroku remote:
   ```bash
   heroku git:remote -a <your-app-name>
   ```
3. Push the code and let Heroku run the build and release steps:
   ```bash
   git push heroku main
   ```
4. Run Django migrations on Heroku:
   ```bash
   heroku run python manage.py migrate
   ```

## Next Steps
- Build out restaurant search models and integrate external APIs for live data.
- Implement authentication for saved places and preferences.
- Connect a mapping library (Mapbox, Leaflet, etc.) to surface location results.
