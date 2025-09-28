# Restaurant Finder

Restaurant Finder is a Django-powered web app that showcases a curated set of Austin restaurants on a Google Maps experience. Users can filter by cuisine, price, rating, and open status and explore locations through an interactive map and synchronized list view.

## Features
- Interactive landing page with Google Maps markers and responsive list view.
- REST-style JSON API for restaurant listing and detail endpoints with flexible filtering.
- Seed command that populates Postgres (or SQLite for local development) with 36 curated Austin restaurants.
- Modern UI with filter controls for cuisine, price tier, minimum rating, and “open now” toggle.
- Heroku-friendly configuration including Whitenoise static serving and environment-driven settings.

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
│   ├── api.py
│   ├── apps.py
│   ├── filters.py
│   ├── fixtures
│   │   └── restaurants.json
│   ├── management
│   │   └── commands
│   │       └── seed_restaurants.py
│   ├── migrations
│   │   └── 0001_initial.py
│   ├── models.py
│   ├── static
│   │   └── restaurants
│   │       ├── css
│   │       │   └── base.css
│   │       └── js
│   │           └── app.js
│   ├── templates
│   │   └── restaurants
│   │       └── home.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── runtime.txt
└── staticfiles/
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
python manage.py seed_restaurants
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` to confirm the map and filters render.

### Environment Variables
Create a `.env` file (or export environment variables) with at least:
```
DJANGO_SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DB_NAME
GOOGLE_MAPS_API_KEY=your-browser-key
```
If `GOOGLE_MAPS_API_KEY` is omitted the page still renders, but the map will fallback to a list-only experience.

### Seeding Data
Use the management command to load or refresh the curated restaurants:
```bash
python manage.py seed_restaurants --clear  # optional --clear removes existing rows first
```
The command is idempotent and will update existing rows based on restaurant name.

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
4. Run Django migrations and seed data on Heroku:
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py seed_restaurants
   ```

## Future Enhancements
- Connect to a live data provider for real-time restaurant availability.
- Persist user sessions and saved favorites.
- Add automated end-to-end testing and accessibility audits.
- Introduce clustering and advanced map interactions as the dataset grows.
