from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.test import TestCase, override_settings
import pytest

from media_guard.backends.nginx import MediaGuardNginxBackend
from media_guard.exceptions import MediaguardMissingBackend
from media_guard.views import MediaGuardBaseView


class TestMediaGuardBaseView:
    def test_requires_mediaguard_backend_setting(self):
        """Raise an ImproperlyConfigured exception when missing setting."""
        del settings.MEDIAGUARD_BACKEND
        with pytest.raises(ImproperlyConfigured):
            MediaGuardBaseView()

    @override_settings(MEDIAGUARD_BACKEND="MediaGuardNginxBackend")
    def test_loads_correct_backend(self):
        """The view should load the correct backend when set."""
        assert isinstance(MediaGuardBaseView().backend, MediaGuardNginxBackend)

    @override_settings(MEDIAGUARD_BACKEND="MediaGuardNetscapeNavigatorBackend")
    def test_handles_missing_backend(self):
        """Raise approprate exception when backend is not present."""
        with pytest.raises(MediaguardMissingBackend):
            MediaGuardBaseView()
