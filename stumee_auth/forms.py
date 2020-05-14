from django import forms
from . import models

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = ('username', 'original_image',)
