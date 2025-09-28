"""Queryset filtering utilities for restaurant searches."""
from __future__ import annotations

from typing import Iterable

from django.db.models import QuerySet

from .models import Restaurant


def parse_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    truthy = {"1", "true", "yes", "on"}
    falsy = {"0", "false", "no", "off"}
    lowered = value.lower()
    if lowered in truthy:
        return True
    if lowered in falsy:
        return False
    return None


def _normalize_cuisines(raw: str | None) -> list[str]:
    if not raw:
        return []
    cuisines: list[str] = []
    for item in raw.split(","):
        item = item.strip().lower()
        if item:
            cuisines.append(item)
    return cuisines


def apply_filters(queryset: QuerySet[Restaurant], params: dict[str, str]) -> QuerySet[Restaurant]:
    cuisines = _normalize_cuisines(params.get("cuisine"))
    if cuisines:
        queryset = queryset.filter(cuisine__in=cuisines)

    price_value = params.get("price")
    if price_value:
        try:
            price_int = int(price_value)
        except (TypeError, ValueError):
            price_int = None
        if price_int in {1, 2, 3, 4}:
            queryset = queryset.filter(price_tier=price_int)

    rating_min = params.get("rating_min")
    if rating_min:
        try:
            rating_float = float(rating_min)
        except (TypeError, ValueError):
            rating_float = None
        if rating_float is not None:
            queryset = queryset.filter(average_rating__gte=rating_float)

    open_now = parse_bool(params.get("open_now"))
    if open_now is not None:
        queryset = queryset.filter(is_open_now=open_now)

    return queryset.order_by("-average_rating", "name")


__all__: Iterable[str] = ["apply_filters", "parse_bool"]
