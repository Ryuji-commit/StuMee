from django import forms

from . import models


class CreateCourseForm(forms.ModelForm):

    class Meta:
        model = models.Course
        fields = ('title', 'description', 'category', 'staffs')


class CreateCategoryForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = ('name', )
        labels = {
            'name': 'Category名',
        }


class UpdateCourseForm(forms.ModelForm):

    class Meta:
        model = models.Course
        fields = ('title', 'description', 'category', 'staffs')
