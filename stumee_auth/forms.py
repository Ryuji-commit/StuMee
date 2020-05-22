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
