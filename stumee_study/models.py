from django.db import models

from stumee_auth.models import CustomUser
from datetime import datetime
# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    make_date = models.DateTimeField(default=datetime.now)
    create_user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, default=1, related_name='create_user')
    staffs = models.ManyToManyField(CustomUser, related_name='staffs')
    course_image = models.ImageField(
        upload_to='course_icon',
        verbose_name='コースアイコン',
        blank=True,
        default='default_icon/default_icon1.png',
    )
