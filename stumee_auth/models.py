from django.db import models
from django.contrib.auth.models import AbstractUser

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
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

    # 0=student, 1=TA, 2=teacher
    UserAuth = [
        (0, 'student'),
        (1, 'TA'),
        (2, 'teacher'),
    ]

    user_auth = models.IntegerField(verbose_name='権限', default=0, choices=UserAuth)


class CertificationPass(models.Model):
    login_certification_key = models.CharField(max_length=10)

    def __str__(self):
        return self.login_certification_key

