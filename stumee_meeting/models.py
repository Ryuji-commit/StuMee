from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager

from stumee_auth.models import CustomUser
from datetime import datetime
# Create your models here.


class Thread(models.Model):
    title = models.CharField('タイトル', max_length=50)
    description = models.TextField('本文', max_length=200)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, default=1)
    make_date = models.DateTimeField(default=datetime.now)
    tag = TaggableManager(blank=True)
    good_count = models.IntegerField(default=0)
    is_picked = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    no = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)], default=1)
    comment = models.TextField('コメント', max_length=200)
    up_date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, default=1)
    good_count = models.IntegerField(default=0)


class ThreadGood(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, default=1)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)


class CommentGood(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, default=1)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class CommentToComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_to_comment')
    comment_to_comment = models.TextField('コメント', max_length=200)
    up_date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, default=1)
