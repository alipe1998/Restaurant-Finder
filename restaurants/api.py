"""JSON API views for the restaurant catalogue."""
from __future__ import annotations

from typing import Any

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404

from .filters import apply_filters
from .models import Restaurant

DEFAULT_PAGE_SIZE = 20


def _serialize_restaurant(restaurant: Restaurant) -> dict[str, Any]:
    return {
        "id": restaurant.id,
        "name": restaurant.name,
        "cuisine": restaurant.get_cuisine_display(),
        "cuisine_key": restaurant.cuisine,
        "price_tier": restaurant.price_tier,
        "price_symbols": restaurant.price_symbols,
        "average_rating": float(restaurant.average_rating),
        "is_open_now": restaurant.is_open_now,
        "status_text": restaurant.status_text,
        "latitude": float(restaurant.latitude),
        "longitude": float(restaurant.longitude),
        "address": restaurant.address,
        "phone": restaurant.phone,
        "website": restaurant.website,
        "short_description": restaurant.short_description,
        "hours": restaurant.hours,
    }


def restaurants_list(request: HttpRequest) -> JsonResponse:
    queryset = apply_filters(Restaurant.objects.all(), request.GET)
    page_number = request.GET.get("page", "1")
    paginator = Paginator(queryset, DEFAULT_PAGE_SIZE)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages or 1)

    results = [_serialize_restaurant(instance) for instance in page_obj.object_list]
    payload = {
        "count": paginator.count,
        "page": page_obj.number,
        "num_pages": paginator.num_pages,
        "results": results,
    }
    return JsonResponse(payload)


def restaurant_detail(request: HttpRequest, pk: int) -> JsonResponse:
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return JsonResponse(_serialize_restaurant(restaurant))
