from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin

from example.models import DownloadableFile, Item
from media_guard.views import MediaGuardViewFile


class DownloadableFileView(SingleObjectMixin, MediaGuardViewFile):
    """Simple asset view for the purposes of development."""

    model = DownloadableFile

    def dispatch(self, request, *args, **kwargs):
        """Ensure the object is loaded on all dispatched method calls."""
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def handle_permission_denied(self, request, *args, **kwargs):
        """Redirect to relevant login or product page on permission denied.

        Returns a response object.
        """
        if request.user.is_authenticated:
            # If the user is logged in, attempt to redirect to a product page.
            # If a product page does not exist, we raise a raw 403 to indicate that
            # the file is there but no licence is owned.
            try:
                product = Item.objects.get(asset=self.object.asset)
            except Item.DoesNotExist:
                raise PermissionDenied()
            messages.warning(request, "You do not currently own a copy of this asset.")
            return redirect(reverse("item_detail", kwargs={"pk": product.pk}))
        messages.warning(request, "You must be logged in to view this.")
        return redirect(reverse("users:login"))

    def has_required_user_permissions(self, request, *args, **kwargs):
        """Test the is_public user permission."""
        if request.user.is_superuser:
            return True

        if self.object.is_public:
            return True
        elif not request.user.is_authenticated():
            return False
        return super().has_required_user_permissions(request, *args, **kwargs)

    def get_media_file_path(self, request, *args, **kwargs):
        """Return the FileAsset object relative path."""
        return self.object.file


class ItemDetail(DetailView):
    model = Item


class ItemList(ListView):
    model = Item
