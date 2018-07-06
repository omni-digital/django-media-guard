from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.functional import cached_property

from media_guard.models import GuardedAsset
from media_guard.storage import ProtectedFileSystemStorage


class Asset(models.Model):
    """Model representation of a asset."""
    name = models.CharField(max_length=256, verbose_name='name')
    description = models.TextField(blank=True, verbose_name='description')
    download_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    def get_absolute_url(self):
        """Return a reversed URL for the asset."""
        return reverse('asset_view', kwargs={'pk': self.pk})


class DownloadableFile(GuardedAsset, models.Model):
    """File available to those who have access to an asset."""
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='related_files',
    )
    file = models.FileField(
        upload_to='assets',
        storage=ProtectedFileSystemStorage()
    )
    name = models.CharField(
        max_length=512,
        help_text='An internal name for the purposes of searching.'
    )

    @cached_property
    def protected_url_path(self):
        """Return a reversed URL for the protected asset."""
        return reverse('asset_view', kwargs={'pk': self.pk})

    @cached_property
    def protected_url_html(self):
        """Return the HTML for a protected_url."""
        return format_html('<a href="{0}" target="_blank">{1}</a>'.format(
            self.protected_url_path, self.protected_url_path
        ))


class Item(models.Model):
    """Model representation of product."""
    name = models.CharField(max_length=256, verbose_name='name')
    description = models.TextField(blank=True, verbose_name='description')
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='downloadable_files',
    )
