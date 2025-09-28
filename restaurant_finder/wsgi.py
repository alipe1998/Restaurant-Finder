"""WSGI config for Restaurant Finder."""
from __future__ import annotations

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant_finder.settings")

application = get_wsgi_application()
