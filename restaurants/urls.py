"""URL declarations for the restaurants app."""
from __future__ import annotations

from django.urls import path

from . import api, views

app_name = "restaurants"

urlpatterns = [
    path("", views.home, name="home"),
    path("api/restaurants/", api.restaurants_list, name="restaurants-list"),
    path("api/restaurants/<int:pk>/", api.restaurant_detail, name="restaurants-detail"),
]
