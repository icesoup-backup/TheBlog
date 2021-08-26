from django.contrib.auth.models import User
from django.db.models import fields
from django.forms.widgets import HiddenInput
from .models import Comment, Post
from django import forms
from django_summernote.widgets import SummernoteWidget
from django.utils.text import slugify


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = HiddenInput()
        self.fields['body'].label = ''


class PostForm(forms.ModelForm):
    # instead of forms.Textarea
    content = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Post
        fields = ('content',)


class NewPostForm(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Post
        fields = ('author', 'title', 'slug', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].disabled = True

