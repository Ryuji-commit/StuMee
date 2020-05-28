from django.db import models

from stumee_auth.models import CustomUser
from datetime import datetime
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    make_date = models.DateTimeField(default=datetime.now)
    create_user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, default=1, related_name='create_user')
    staffs = models.ManyToManyField(CustomUser, related_name='staffs')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
