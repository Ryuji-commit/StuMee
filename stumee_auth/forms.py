from django import forms
from . import models


class ProfileForm(forms.ModelForm):
    original_image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = models.CustomUser
        fields = ('username', 'original_image',)
        labels = {
            'username': 'ユーザ名',
            'original_image': 'アイコン',
        }
