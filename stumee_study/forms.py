from django import forms

from . import models


class CreateCourseForm(forms.ModelForm):

    class Meta:
        model = models.Course
        fields = ('title', 'description',)
