import os

from django.core.wsgi import get_wsgi_application

# Use environment variable, fallback to local for development
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aimarketing.settings.production")

application = get_wsgi_application()
