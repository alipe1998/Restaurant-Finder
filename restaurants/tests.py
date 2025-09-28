"""Smoke tests for the restaurants app."""
from __future__ import annotations

from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse

from .filters import apply_filters
from .models import Restaurant


class HomeViewTests(TestCase):
    def setUp(self) -> None:
        Restaurant.objects.create(
            name="Test Cafe",
            cuisine=Restaurant.Cuisine.CAFE,
            price_tier=2,
            average_rating=Decimal("4.5"),
            is_open_now=True,
            latitude=Decimal("30.0"),
            longitude=Decimal("-97.0"),
            address="123 Main St",
            phone="",
            website="",
            short_description="A cozy cafe for tests.",
            hours={},
        )

    def test_home_page_renders(self) -> None:
        response = self.client.get(reverse("restaurants:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Restaurant Finder")
        self.assertContains(response, "Cuisine")


class RestaurantFilterTests(TestCase):
    def setUp(self) -> None:
        Restaurant.objects.bulk_create(
            [
                Restaurant(
                    name="Open Sushi",
                    cuisine=Restaurant.Cuisine.SUSHI,
                    price_tier=3,
                    average_rating=Decimal("4.8"),
                    is_open_now=True,
                    latitude=Decimal("30.1"),
                    longitude=Decimal("-97.1"),
                    address="1 Sushi Way",
                    phone="",
                    website="",
                    short_description="",
                    hours={},
                ),
                Restaurant(
                    name="Closed BBQ",
                    cuisine=Restaurant.Cuisine.BARBECUE,
                    price_tier=2,
                    average_rating=Decimal("4.0"),
                    is_open_now=False,
                    latitude=Decimal("30.2"),
                    longitude=Decimal("-97.2"),
                    address="2 Smoke St",
                    phone="",
                    website="",
                    short_description="",
                    hours={},
                ),
            ]
        )

    def test_filter_by_cuisine(self) -> None:
        queryset = Restaurant.objects.all()
        filtered = apply_filters(queryset, {"cuisine": "sushi"})
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first().name, "Open Sushi")

    def test_filter_by_open_now(self) -> None:
        queryset = Restaurant.objects.all()
        filtered = apply_filters(queryset, {"open_now": "true"})
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first().name, "Open Sushi")


class RestaurantAPITests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        Restaurant.objects.create(
            name="API Test Pizza",
            cuisine=Restaurant.Cuisine.PIZZA,
            price_tier=2,
            average_rating=Decimal("4.2"),
            is_open_now=True,
            latitude=Decimal("30.3"),
            longitude=Decimal("-97.3"),
            address="3 Slice Ave",
            phone="512-555-0000",
            website="https://apitestpizza.example.com",
            short_description="Pizza for API tests.",
            hours={"monday": "11:00-22:00"},
        )

    def test_restaurants_list_endpoint(self) -> None:
        response = self.client.get(reverse("restaurants:restaurants-list"))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("results", payload)
        self.assertGreaterEqual(payload["count"], 1)

    def test_restaurant_detail_endpoint(self) -> None:
        restaurant = Restaurant.objects.get(name="API Test Pizza")
        response = self.client.get(
            reverse("restaurants:restaurants-detail", args=[restaurant.pk])
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["name"], "API Test Pizza")
        self.assertEqual(payload["cuisine"], "Pizza")
