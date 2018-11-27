from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.test import TestCase, override_settings, RequestFactory

from media_guard.backends.nginx import MediaGuardNginxBackend


class NginxBackendTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.file_path = "/dev/null/super-secret-DONOTSTEAL/my-protected-file.bak1.tiff"
        self.backend = MediaGuardNginxBackend()

    @override_settings()
    def test_raises_improperly_configured(self):
        """Should raise ImproperlyConfigured exception if MEDIAGUARD_URL not set."""
        del settings.MEDIAGUARD_URL
        with self.assertRaises(ImproperlyConfigured):
            MediaGuardNginxBackend()

    def test_attaches_x_accel_redirect_header(self):
        """Test that the X-Accel-Redirect header is present from the backend."""
        response = self.backend.serve(self.request, self.file_path)
        self.assertIn("X-Accel-Redirect", response)

    @override_settings(MEDIAGUARD_URL="/nginx-location", MEDIAGUARD_ROOT="/dev/null")
    def test_x_accel_redirect_header_path(self):
        """Test the path of the header is as expected.

        The location should be relative with the MEDIAGUARD_URL acting as the
        NGINX location namespace to direct the internal redirect.
        """
        response = self.backend.serve(self.request, self.file_path)
        self.assertEqual(
            response["X-Accel-Redirect"],
            "/nginx-location/super-secret-DONOTSTEAL/my-protected-file.bak1.tiff",
        )
