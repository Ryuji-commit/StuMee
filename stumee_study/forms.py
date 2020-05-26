from django import forms

from . import models


class CreateCourseForm(forms.ModelForm):

    class Meta:
        model = models.Course
        fields = ('title', 'description', 'category')


class CreateCategoryForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = ('name', )
        labels = {
            'name': 'Category名',
        }