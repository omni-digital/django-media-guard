import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "media_guard",
    }
}

INSTALLED_APPS = [
    "example",
    "media_guard",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
]

MIDDLEWARE_CLASSES = []

ROOT_URLCONF = "example.urls"

SECRET_KEY = "test"

# Media Guard settings
MEDIAGUARD_URL = "/protected_media"
MEDIAGUARD_ROOT = os.path.join(BASE_DIR, "..", "..", "protected_media")
MEDIAGUARD_BACKEND = "MediaGuardDjangoBackend"
