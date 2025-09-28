# Restaurant Finder — Implementation Plan

This document captures the decisions and deliverables for building the Restaurant Finder MVP with Django, Postgres, and a Google Maps–powered frontend. Codex Cloud can use this plan as the backlog for execution.

## 1. Scope & Assumptions
- Live third-party APIs are **out of scope** for the MVP; we seed Postgres with curated fake data.
- Users interact with a map-first UI that supports filtering by cuisine, price, rating, and open status.
- No user accounts or persistence of favorites for the initial release.
- Heroku hosts both the web app and the managed Postgres database; a single environment (no separate staging).
- Testing is minimal: smoke checks to ensure key endpoints and templates render.

## 2. Data Model & Seed Strategy
### 2.1 Schema
Create the following tables (Django models):
- `Restaurant`: name, cuisine (enum/choice), price tier (1–4), average rating (float), is_open_now (bool), coordinates (Point or lat/lng fields), address, phone, website, short description, hours (JSON/text).
- `Tag` (optional stretch): normalized table for additional labels; relationship via `ManyToManyField` if needed later.

### 2.2 Fake Data
- Author a Django management command `seed_restaurants` that loads a JSON/CSV fixture into the database.
- Store the seed data in `restaurants/fixtures/restaurants.json` with ~25–50 diverse entries spanning cuisines, price tiers, and ratings.
- For geospatial coordinates, use lat/lng pairs within a focus city (e.g., Austin) to simplify the map viewport.
- Command flow:
  ```bash
  python manage.py migrate
  python manage.py seed_restaurants --clear  # optional flag to wipe existing rows
  ```
  The command should support idempotent re-seeding.

## 3. Backend API & Filtering
### 3.1 Endpoints
- `GET /api/restaurants/`: returns paginated list of restaurants with query params:
  - `cuisine` (single or comma-separated list)
  - `price` (single integer 1–4)
  - `rating_min` (float threshold)
  - `open_now` (bool)
- `GET /api/restaurants/<id>/`: returns detail payload.

### 3.2 Filtering Logic
- Implement queryset filters in a dedicated service/helper (easier to unit test).
- Support multiple cuisine selections via `__in` lookup.
- `rating_min` maps to `average_rating__gte`.
- `open_now=true` filters on `is_open_now`.
- Default ordering: `-average_rating`, tie-breaker by `name`.

### 3.3 Response Shape
Return JSON containing `id`, display fields, coordinates, and computed metadata (e.g., price symbols, friendly status string). Keep payload light for map rendering.

## 4. Frontend Map Experience
### 4.1 Stack Choices
- Use Google Maps JavaScript API for map rendering and markers.
- Integrate filters in a sidebar or overlay; selections trigger fetches against `/api/restaurants/`.
- Initial map center and zoom based on dataset centroid; adjust when filters change.

### 4.2 Directions Support
- Google Maps Directions API integration requires additional effort (separate API key scope, UI for origin/destination, extra latency).
- Since ease is uncertain, **omit directions** from the MVP; revisit once core flows stabilize.

### 4.3 UI Components
- `MapView`: initializes Google Map, manages markers, listens for filter updates.
- `FiltersPanel`: dropdowns or chips for cuisine, slider/dropdown for rating, toggle for open now, segmented buttons for price.
- `RestaurantList`: optional list view synchronized with map markers (hover highlights marker).

## 5. Django Views & Routing
- SPA-like flow using a single Django template rendering the filters and map container; hydrate with basic config (API key, initial filters) via template context.
- Serve static JS/CSS bundles. For simplicity, start with vanilla JS or sprinkle Alpine/HTMX; add React/Vue later if needed.
- API endpoints handled via Django REST Framework or custom Django views returning `JsonResponse`. If DRF is preferred, add it to requirements.

## 6. Deployment Pipeline
### 6.1 Heroku Setup
1. Create Heroku app: `heroku create restaurant-finder-app`.
2. Provision Postgres: `heroku addons:create heroku-postgresql:hobby-dev`.
3. Capture DATABASE_URL from Heroku and rely on `dj_database_url` in settings.
4. Configure config vars:
   - `DJANGO_SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS` (include Heroku domain)
   - `GOOGLE_MAPS_API_KEY`
5. Push to Heroku: `git push heroku main` (ensure collectstatic with Whitenoise succeeds).
6. Run migrations and seed command on Heroku:
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py seed_restaurants
   ```

### 6.2 Continuous Deployment
- Optional: enable GitHub auto-deploy on Heroku once repo is public.
- Manual deploys are acceptable for MVP.

## 7. Local Development Workflow
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. Create `.env` from `.env.example`; set `DATABASE_URL` to local Postgres or fallback to SQLite for convenience.
4. `python manage.py migrate`
5. `python manage.py seed_restaurants`
6. `python manage.py runserver`

## 8. Future Enhancements (Post-MVP)
- Replace fake data with live API calls (wrap provider in service layer, add caching, handle quotas).
- Add user accounts and favorite lists.
- Implement directions once value is validated.
- Introduce background jobs for nightly data refresh.
- Build automated tests (unit + integration + e2e with Playwright).
- Add staging environment and CI/CD pipeline when team grows.

---
This plan balances quick delivery with a clear path to richer features later. Let me know if any assumptions need adjusting before submission to Codex Cloud.
