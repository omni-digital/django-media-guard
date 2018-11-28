from collections import namedtuple
from os import path
from mimetypes import guess_type
from unicodedata import normalize as unicode_normalize

from django.conf import settings
from django.core import exceptions
from django.http import HttpResponseNotFound
from django.utils.encoding import force_text
from django.utils.http import urlquote
from django.views import View

from media_guard import backends
from media_guard.exceptions import MediaguardMissingBackend


FileMetadata = namedtuple("FileMetadata", ["mimetype", "encoding"])


class MediaGuardBaseView(View):
    """Base Media Guard view.

    Intended to be subclassed by your domain specific integration. Checks that
    the request user has permissions to view the file, if they do this class
    calculates the various Content Headers required to correctly serve it,
    then serves it.
    """

    DEFAULT_MIMETYPE = "application/octet-stream"

    file_info = None
    abs_media_path = ""
    rel_media_path = ""

    # a list of user permissions to check against
    required_user_permissions = []
    # the relative path to the protected media file
    media_file_path = ""
    # optional hardcoded mimetype
    media_mimetype_override = ""
    media_encoding = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(settings, "MEDIAGUARD_BACKEND"):
            raise exceptions.ImproperlyConfigured(
                "MEDIAGUARD_BACKEND not configured in settings."
            )

        if not hasattr(backends, settings.MEDIAGUARD_BACKEND):
            raise MediaguardMissingBackend(
                "MEDIAGUARD_BACKEND is set to a backend which does not exist."
            )

        self.backend = getattr(backends, settings.MEDIAGUARD_BACKEND)()

    def has_permissions(self, request, *args, **kwargs):
        """
        Iterate through all specified user permissions and check that they are present on
        the user.

        TODO: consider removing, this may be too assumptive of how the package is used?
        """
        if not self.required_user_permissions:
            return False

        # return True if all required user permissions have been met
        return any(
            [
                request.user.has_perm(permission)
                for permission in self.required_user_permissions
            ]
        )

    def get_media_file_path(self, request, *args, **kwargs) -> str:
        """Load the protected media file path relative to settings.MEDIAGUARD_ROOT."""
        if self.media_file_path == "":
            raise ValueError(
                "Media file path not configured and method not overridden."
            )

        return self.media_file_path

    def get_media_mimetype(self, guessed_mimetype=None) -> str:
        """
        Return mimetype if set, if not return the guessed mimetype OR
        application/octet-stream as the fallback.
        """
        if self.media_mimetype_override:
            return self.media_mimetype_override

        if not guessed_mimetype:
            return self.DEFAULT_MIMETYPE

        return guessed_mimetype

    def get_media_encoding(self, guessed_encoding="") -> str:
        """Return hardcoded mimetype if set, else return the encoding guessed."""
        if self.media_encoding:
            return self.media_encoding

        # TODO default encoding?
        return guessed_encoding

    def get_file_information(self, file_path) -> FileMetadata:
        """Load file metadata into the FileMetadata named tuple."""
        guessed_mimetype, guessed_encoding = guess_type(file_path)
        mimetype = self.get_media_mimetype(guessed_mimetype=guessed_mimetype)
        encoding = self.get_media_encoding(guessed_encoding=guessed_encoding)
        return FileMetadata(mimetype=mimetype, encoding=encoding)

    def handle_permission_denied(self, request, *args, **kwargs):
        """Handler when a user does not have permission to access.

        Must either raise or return a response object.
        """
        raise exceptions.PermissionDenied()

    def dispatch(self, request, *args, **kwargs):
        """Common file checking and loading functionality."""
        if not self.has_permissions(request, *args, **kwargs):
            return self.handle_permission_denied(request, *args, **kwargs)

        # get our media path relative to the media root
        self.rel_media_path = self.get_media_file_path(request, *args, **kwargs)

        # load the absolute path
        self.abs_media_path = path.abspath(
            path.join(settings.MEDIAGUARD_ROOT, self.rel_media_path)
        )
        self._traversal_guard()

        if not path.exists(self.abs_media_path):
            return HttpResponseNotFound()

        self.file_info = self.get_file_information(self.abs_media_path)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Load the file into the response."""
        response = self.backend.serve(request, self.abs_media_path)
        response["Content-Type"] = self.file_info.mimetype
        response["Content-Length"] = path.getsize(self.abs_media_path)
        response["Content-Encoding"] = self.file_info.encoding
        return response

    def _traversal_guard(self):
        """
        Check the absolute path of the MEDIAGUARD_ROOT against the abs path
        from the file.

        Ensures that nothing nasty is attempted for serving files outside the
        scope of the root folder.
        """
        abs_mediaguard_root = path.abspath(settings.MEDIAGUARD_ROOT)
        if not path.commonpath([abs_mediaguard_root]) == path.commonpath(
            [abs_mediaguard_root, self.abs_media_path]
        ):
            raise exceptions.SuspiciousFileOperation(
                "Potential directory traversal attack"
            )


class MediaGuardInspectView(MediaGuardBaseView):
    pass


class MediaGuardDownloadView(MediaGuardBaseView):
    """Download file instead of viewing.."""

    def get_filename(self, filepath):
        return force_text(path.basename(filepath))

    def get_ascii_filename(self, filename):
        return unicode_normalize("NFKD", filename).encode("ascii", "ignore")

    def get_parts(self, *args, **kwargs):
        """Calculate the content disposition parts."""
        parts = ["attachment"]
        filename = self.get_filename(self.abs_media_path)
        unicode_filename = self.get_ascii_filename(filename)
        parts.append("filename={}".format(unicode_filename))
        if filename != unicode_filename:
            parts.append("filename*=UTF-8''{}".format(urlquote(filename)))
        return parts

    def get(self, request, *args, **kwargs):
        """
        Perform base view actions, then calculate the content disposition for
        the response.
        """
        response = super().get(request, *args, **kwargs)
        response["Content-Disposition"] = "; ".join(self.get_parts(*args, **kwargs))
        return response
