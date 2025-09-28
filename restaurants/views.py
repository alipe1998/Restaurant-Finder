"""HTTP views for the Restaurant Finder landing page."""
from __future__ import annotations

import json

from django.conf import settings
from django.db.models import Avg
from django.shortcuts import render
from django.urls import reverse

from .models import Restaurant

AUSTIN_DEFAULT_CENTER = {"lat": 30.2672, "lng": -97.7431}


def home(request):
    restaurants = Restaurant.objects.all()
    averages = restaurants.aggregate(avg_lat=Avg("latitude"), avg_lng=Avg("longitude"))
    center = {
        "lat": float(averages["avg_lat"]) if averages["avg_lat"] is not None else AUSTIN_DEFAULT_CENTER["lat"],
        "lng": float(averages["avg_lng"]) if averages["avg_lng"] is not None else AUSTIN_DEFAULT_CENTER["lng"],
    }

    cuisines = [
        {"key": key, "label": label}
        for key, label in Restaurant.Cuisine.choices
    ]

    price_tiers = [
        {"value": tier, "label": "$" * tier}
        for tier in range(1, 5)
    ]

    config = {
        "apiBaseUrl": reverse("restaurants:restaurants-list"),
        "mapCenter": center,
    }

    context = {
        "page_title": "Restaurant Finder",
        "google_maps_api_key": getattr(settings, "GOOGLE_MAPS_API_KEY", ""),
        "price_tiers": price_tiers,
        "cuisines": cuisines,
        "config_json": json.dumps(config),
    }
    return render(request, "restaurants/home.html", context)
