from django.db import models
from django.contrib.auth.models import AbstractUser

from django_cleanup import cleanup
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
@cleanup.ignore
class CustomUser(AbstractUser):
    original_image = models.ImageField(
        upload_to='user_icon/',
        verbose_name='オリジナルアイコン',
        blank=True,
        default='default_icon/default_icon1.png',
    )

    big = ImageSpecField(
        source="original_image",
        processors=[ResizeToFill(300, 300)],
        format='JPEG'
    )

    small = ImageSpecField(
        source='original_image',
        processors=[ResizeToFill(50, 50)],
        format="JPEG",
        options={'quality': 75}
    )


