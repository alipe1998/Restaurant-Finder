"""ASGI config for Restaurant Finder."""
from __future__ import annotations

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant_finder.settings")

application = get_asgi_application()
