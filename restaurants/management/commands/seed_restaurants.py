"""Seed the database with curated restaurant data."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from restaurants.models import Restaurant

FIXTURE_PATH = Path("restaurants/fixtures/restaurants.json")


class Command(BaseCommand):
    help = "Load the curated restaurant catalogue into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing restaurants before seeding.",
        )

    def handle(self, *args: Any, **options: Any):
        if not FIXTURE_PATH.exists():
            raise CommandError(f"Fixture file not found at {FIXTURE_PATH}")

        with FIXTURE_PATH.open() as source:
            data = json.load(source)

        if not isinstance(data, list):
            raise CommandError("Expected a list of restaurants in the fixture file.")

        with transaction.atomic():
            if options.get("clear"):
                deleted, _ = Restaurant.objects.all().delete()
                self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing restaurants."))

            created = 0
            updated = 0
            for entry in data:
                defaults = {
                    "cuisine": entry["cuisine"],
                    "price_tier": entry["price_tier"],
                    "average_rating": entry["average_rating"],
                    "is_open_now": entry["is_open_now"],
                    "latitude": entry["latitude"],
                    "longitude": entry["longitude"],
                    "address": entry["address"],
                    "phone": entry.get("phone", ""),
                    "website": entry.get("website", ""),
                    "short_description": entry["short_description"],
                    "hours": entry.get("hours", {}),
                }
                obj, created_flag = Restaurant.objects.update_or_create(
                    name=entry["name"], defaults=defaults
                )
                if created_flag:
                    created += 1
                else:
                    updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete. Created {created} and updated {updated} restaurant records."
            )
        )
