from django import forms

from . import models


class CreateCourseForm(forms.ModelForm):

    class Meta:
        model = models.Course
        fields = ('title', 'description', 'category', 'staffs', 'certification_key')


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
        fields = ('title', 'description', 'category', 'staffs', 'certification_key')


class CourseCertificationForm(forms.Form):
    certification_password_course = forms.CharField(
        label='コース認証コード',
        required=True,
        disabled=False,
        max_length=10,
        min_length=1,
        widget=forms.PasswordInput(attrs={
            'id': 'id_course_password',
            'placeholder': '半角英数字のみ入力可能です。',
            'pattern': '^[A-Za-z0-9]+$'})
    )
