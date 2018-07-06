from django.db import models


class GuardedAsset(models.Model):
    """A Guarded Asset is one that may have some form of limited access.

    TODO: potentially build in support for this at the view level?
    """

    is_public = models.BooleanField(default=False)

    class Meta:
        abstract = True
