from os import path

from django.views.static import serve as static_serve


class MediaGuardDjangoBackend:
    """
    Django staticfiles backend for MediaGuard.

    Simply serves the file using django's staticfiles function.
    """

    def serve(self, request, file_path, *args, **kwargs):
        """Backend serve command for serving the asset as a response."""
        dirname = path.dirname(file_path)
        basename = path.basename(file_path)
        return static_serve(request, basename, dirname)
