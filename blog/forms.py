from django.forms.widgets import HiddenInput
from .models import Comment, Post
from django import forms
from django_summernote.widgets import SummernoteWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        # fields = ('name', 'body', 'post')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget = HiddenInput()
        # self.fields['post'].widget = HiddenInput()
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

