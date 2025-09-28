"""HTTP views for the Restaurant Finder landing page."""
from __future__ import annotations

from django.shortcuts import render


def home(request):
    return render(request, "restaurants/home.html", {"page_title": "Restaurant Finder"})
