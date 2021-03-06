from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from stumee_study.models import Course
from stumee_auth.models import CustomUser


# Create your models here.
class Channel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, default=1)
    is_discussion = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    problem_being_solved = models.IntegerField(blank=True, null=True)


class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, default=1)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
