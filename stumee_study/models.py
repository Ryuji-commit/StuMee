from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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
    staffs = models.ManyToManyField(CustomUser, related_name='staffs', blank=True, default=None)
    students = models.ManyToManyField(CustomUser, related_name='students', blank=True, default=None)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    certification_key = models.CharField(max_length=10, null=True)
    problem_nums = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(50)])

    def __str__(self):
        return self.title
