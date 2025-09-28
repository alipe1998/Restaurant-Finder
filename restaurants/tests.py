"""Smoke tests for the restaurants app."""
from __future__ import annotations

from django.test import SimpleTestCase
from django.urls import reverse


class HomeViewTests(SimpleTestCase):
    def test_home_page_renders(self) -> None:
        response = self.client.get(reverse("restaurants:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Restaurant Finder")
