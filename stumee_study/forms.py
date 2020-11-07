from django import forms

from . import models


class CreateCourseForm(forms.ModelForm):

    class Meta:
        model = models.Course
        fields = ('title', 'description', 'category', 'staffs', 'certification_key', 'problem_nums')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TAに絞り込む
        self.fields['staffs'].queryset = self.fields['staffs'].queryset.filter(user_auth__gte=1)
        self.fields['staffs'].widget.attrs = {'data-toggle': 'tooltip',
                                              'title': 'TAを選択してください<br>Ctrl+クリックで複数選択が可能です',
                                              'data-html': 'true'}
        self.fields['category'].widget.attrs = {'data-toggle': 'tooltip',
                                                'title': '受講する学生の学年を選んでください'}
        self.fields['problem_nums'].widget.attrs = {'data-toggle': 'tooltip',
                                                    'title': '問題数を入力してください。これはオプションです。'}
        self.fields['certification_key'].widget.attrs = {'data-toggle': 'tooltip',
                                                         'title': '認証キーを設定してください<br>'
                                                                  '学生がコースに登録する際に必要です',
                                                         'data-html': 'true',
                                                         'placeholder': '半角英数字のみ入力可能です。',
                                                         'pattern': '^[A-Za-z0-9]+$'}


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
        fields = ('title', 'description', 'category', 'staffs', 'certification_key', 'problem_nums')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TAに絞り込む
        self.fields['staffs'].queryset = self.fields['staffs'].queryset.filter(user_auth__gte=1)
        self.fields['staffs'].widget.attrs = {'data-toggle': 'tooltip',
                                              'title': 'TAを選択してください<br>Ctrl+クリックで複数選択が可能です',
                                              'data-html': 'true'}
        self.fields['category'].widget.attrs = {'data-toggle': 'tooltip',
                                                'title': '受講する学生の学年を選んでください'}
        self.fields['problem_nums'].widget.attrs = {'data-toggle': 'tooltip',
                                                    'title': '問題数を入力してください。これはオプションです。'}
        self.fields['certification_key'].widget.attrs = {'data-toggle': 'tooltip',
                                                         'title': '認証キーを設定してください<br>'
                                                                  '学生がコースに登録する際に必要です',
                                                         'data-html': 'true',
                                                         'placeholder': '半角英数字のみ入力可能です。',
                                                         'pattern': '^[A-Za-z0-9]+$'}


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
