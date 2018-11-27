from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible


@deconstructible
class ProtectedFileSystemStorage(FileSystemStorage):
    """
    Custom protected file system storage backend.

    Workaround to stop makemigrations from picking up the potentially changing
    settings.MEDIAGUARD_ROOT in a developer's local system settings file.

    Found the workaround here: https://github.com/translate/pootle/issues/3557
    """

    def __init__(self, *args, **kwargs):
        kwargs.update({"location": settings.MEDIAGUARD_ROOT})
        super().__init__(*args, **kwargs)
