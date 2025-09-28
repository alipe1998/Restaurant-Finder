"""Data models for restaurant domain objects."""
from __future__ import annotations

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Restaurant(models.Model):
    """Represents a single restaurant in the catalogue."""

    class Cuisine(models.TextChoices):
        AMERICAN = "american", "American"
        ASIAN_FUSION = "asian_fusion", "Asian Fusion"
        BARBECUE = "barbecue", "Barbecue"
        BAKERY = "bakery", "Bakery"
        BREAKFAST = "breakfast", "Breakfast & Brunch"
        CAFE = "cafe", "Cafe"
        CHINESE = "chinese", "Chinese"
        FINE_DINING = "fine_dining", "Fine Dining"
        FRENCH = "french", "French"
        GREEK = "greek", "Greek"
        INDIAN = "indian", "Indian"
        ITALIAN = "italian", "Italian"
        JAPANESE = "japanese", "Japanese"
        KOREAN = "korean", "Korean"
        LATIN = "latin", "Latin"
        MEDITERRANEAN = "mediterranean", "Mediterranean"
        MEXICAN = "mexican", "Mexican"
        PIZZA = "pizza", "Pizza"
        PUB = "pub", "Pub"
        SEAFOOD = "seafood", "Seafood"
        SOUTHERN = "southern", "Southern"
        STEAKHOUSE = "steakhouse", "Steakhouse"
        SUSHI = "sushi", "Sushi"
        TACOS = "tacos", "Tacos"
        THAI = "thai", "Thai"
        VEGAN = "vegan", "Vegan"
        VIETNAMESE = "vietnamese", "Vietnamese"
        WINE_BAR = "wine_bar", "Wine Bar"

    name = models.CharField(max_length=255)
    cuisine = models.CharField(max_length=32, choices=Cuisine.choices)
    price_tier = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        help_text="Price level on a scale from 1 (budget) to 4 (splurge).",
    )
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    is_open_now = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    short_description = models.CharField(max_length=280)
    hours = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-average_rating", "name"]
        indexes = [
            models.Index(fields=["cuisine"]),
            models.Index(fields=["price_tier"]),
            models.Index(fields=["is_open_now"]),
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name

    @property
    def price_symbols(self) -> str:
        return "$" * self.price_tier

    @property
    def status_text(self) -> str:
        return "Open now" if self.is_open_now else "Closed"
