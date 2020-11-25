from django import forms
from . import models
from taggit.managers import TaggableManager


class ThreadForm(forms.ModelForm):
    class Meta:
        model = models.Thread
        fields = ('title', 'description', 'tag',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('comment',)


class CommentToCommentForm(forms.ModelForm):
    class Meta:
        model = models.CommentToComment
        fields = ('comment_to_comment', 'comment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs['id'] = 'id_parent_comment_select'
        self.fields['comment'].widget.attrs['style'] = 'display:none'


