from os import path

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.http import HttpResponse


class MediaGuardNginxBackend:
    """NGINX backend for MediaGuard."""

    def __init__(self, *args, **kwargs):
        if not hasattr(settings, 'MEDIAGUARD_URL'):
            raise ImproperlyConfigured('MEDIAGUARD_URL not set in settings.')
        super().__init__(*args, **kwargs)

    def serve(self, request, file_path, *args, **kwargs):
        """Backend serve command to pass the header back to NGINX."""
        response = HttpResponse()
        relative_path = path.relpath(file_path, settings.MEDIAGUARD_ROOT)
        response['X-Accel-Redirect'] = settings.MEDIAGUARD_URL + '/' + relative_path
        return response
