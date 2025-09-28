"""URL declarations for the restaurants app."""
from __future__ import annotations

from django.urls import path

from . import views

app_name = "restaurants"

urlpatterns = [
    path("", views.home, name="home"),
]
