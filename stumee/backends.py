from storages.backends.s3boto3 import S3Boto3Storage
from tempfile import SpooledTemporaryFile
import os


class MediaStorage(S3Boto3Storage):
    location = 'media'  # /media というURLで配信
    file_overwrite = False  # 上書きしない

    def _save(self, name, content):
        """
        This method that fixes a bug in boto3 where the passed in file is closed upon upload.
        From:
        https://github.com/matthewwithanm/django-imagekit/issues/391#issuecomment-275367006
        https://github.com/boto/boto3/issues/929
        https://github.com/matthewwithanm/django-imagekit/issues/391
        We create a clone of the content file as when this is passed to
        boto3 it wrongly closes the file upon upload where as the storage
        backend expects it to still be open
        """
        # Seek our content back to the start
        content.seek(0, os.SEEK_SET)

        # Create a temporary file that will write to disk after a specified
        # size. This file will be automatically deleted when closed by
        # boto3 or after exiting the `with` statement if the boto3 is fixed
        with SpooledTemporaryFile() as content_autoclose:
            # Write our original content into our copy that will be closed by boto3
            content_autoclose.write(content.read())

            # Upload the object which will auto close the
            # content_autoclose instance
            return super(MediaStorage, self)._save(name, content_autoclose)
