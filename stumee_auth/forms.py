from django import forms
from . import models


class ProfileForm(forms.ModelForm):
    original_image = forms.ImageField(
        widget=forms.FileInput,
        label='アイコン',
        required=False,
    )

    UserAuth = [
        (0, 'student'),
        (1, 'TA'),
        (2, 'teacher'),
    ]

    user_auth = forms.ChoiceField(
        widget=forms.RadioSelect,
        label='権限',
        choices=UserAuth,
    )

    class Meta:
        model = models.CustomUser
        fields = ('username', 'original_image', 'user_auth')
        labels = {
            'username': 'ユーザ名',
        }


class LoginCertificationForm(forms.Form):
    certification_password_login = forms.CharField(
        label='認証パス',
        required=True,
        disabled=False,
        max_length=10,
        min_length=1,
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'placeholder': '半角英数字のみ入力可能です。',
            'pattern': '^[A-Za-z0-9]+$'})
    )


class ChangeAuthorityToTA(forms.Form):
    certification_password_change_auth_TA = forms.CharField(
        label='与えられた認証パスを入力してください。',
        required=True,
        disabled=False,
        max_length=10,
        min_length=1,
        widget=forms.PasswordInput(attrs=
        {
            'id': 'ta_password',
            'placeholder': '半角英数字のみ入力可能です。',
            'pattern': '^[A-Za-z0-9]+$'
        })
    )


class ChangeAuthorityToTeacher(forms.Form):
    certification_password_change_auth_Teacher = forms.CharField(
        label='与えられた認証パスを入力してください',
        required=True,
        disabled=False,
        max_length=10,
        min_length=1,
        widget=forms.PasswordInput(attrs=
        {
            'id': 'teacher_password',
            'placeholder': '半角英数字のみ入力可能です。',
            'pattern': '^[A-Za-z0-9]+$'
        })
    )

