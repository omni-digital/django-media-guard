from django.forms.widgets import ClearableFileInput
from django.urls import reverse


class ProtectedFileInput(ClearableFileInput):
    """Add additional context to the file input to load the correct asset URL."""
    template_name = 'media_guard/protected_clearable_file_input.html'

    def get_context(self, name, value, attrs):
        """Load the protected asset URL into the context."""
        context = super().get_context(name, value, attrs)
        if value.instance.pk:
            context['protected_asset_url'] = reverse(
                'download',
                kwargs={'pk': value.instance.pk}
            )
        return context
