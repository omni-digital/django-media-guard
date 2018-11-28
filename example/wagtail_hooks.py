"""Assets module Wagtail hooks."""
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from example.models import Asset, DownloadableFile


class AssetAdmin(ModelAdmin):
    """Wagtail Admin integration for `Asset` model."""

    model = Asset
    menu_icon = "media"
    menu_order = 200
    list_display = (
        "name",
        "description",
        "download_url",
        "video_url",
        "created",
        "modified",
    )
    search_fields = ("name",)


modeladmin_register(AssetAdmin)


class DownloadableFileWagtailAdmin(ModelAdmin):
    """Wagtail Admin integration for downloadable files."""

    model = DownloadableFile
    menu_order = 201
    list_display = ("name", "protected_url_html", "asset")


modeladmin_register(DownloadableFileWagtailAdmin)
