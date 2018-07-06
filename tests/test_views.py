from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.test import TestCase, override_settings

from media_guard.backends.nginx import MediaGuardNginxBackend
from media_guard.exceptions import MediaguardMissingBackend
from media_guard.views import MediaGuardViewFile


class MediaGuardViewFileTestCase(TestCase):
    @override_settings()
    def test_requires_mediaguard_backend_setting(self):
        """
        The view should raise an ImproperlyConfigured exception when missing
        MEDIAGUARD_BACKEND setting.
        """
        del settings.MEDIAGUARD_BACKEND
        with self.assertRaises(ImproperlyConfigured):
            MediaGuardViewFile()

    @override_settings(MEDIAGUARD_BACKEND='MediaGuardNginxBackend')
    def test_loads_correct_backend(self):
        """The view should load the correct backend when set."""
        view = MediaGuardViewFile()
        self.assertIsInstance(view.backend, MediaGuardNginxBackend)

    @override_settings(MEDIAGUARD_BACKEND='MediaGuardNetscapeNavigatorBackend')
    def test_handles_missing_backend(self):
        """
        The view should handle missing backends one that doesn't exist is
        requested.
        """
        with self.assertRaises(MediaguardMissingBackend):
            MediaGuardViewFile()
