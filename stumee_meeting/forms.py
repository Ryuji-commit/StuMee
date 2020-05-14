from django import forms
from . import models
from taggit.managers import TaggableManager


class ThreadForm(forms.ModelForm):
    class Meta:
        model = models.Thread
        fields = ('title', 'description', 'tag',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('comment',)

