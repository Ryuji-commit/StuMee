from django import forms
from django.core.files.storage import default_storage


class FileUploadForm(forms.Form):
    file = forms.FileField()

    def save(self):
        upload_file = self.cleaned_data['file']
        file_name = default_storage.save(upload_file.name, upload_file)
        file_url = default_storage.url(file_name)
        return file_url

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs = {'style': 'display:none'}
        self.fields['file'].label = ''
