"""Data models for restaurant domain objects."""
from __future__ import annotations

from django.db import models


class Restaurant(models.Model):
    """Placeholder model for future restaurant records."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name
