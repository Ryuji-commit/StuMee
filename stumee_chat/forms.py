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


class ProblemNumsUploadForm(forms.Form):
    problem_being_solved = forms.ChoiceField(
        label="進行度",
        required=False,
        widget=forms.widgets.Select(attrs={'class': 'form-control',
                                           'data-toggle': 'tooltip',
                                           'title': '現在取り組んでいる問題番号を選択'}),
    )
