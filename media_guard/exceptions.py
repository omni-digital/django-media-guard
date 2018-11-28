from django.core.exceptions import ImproperlyConfigured


class MediaguardMissingBackend(ImproperlyConfigured):
    """Exception thrown when a backend that doesn't exist is requested."""

    pass
