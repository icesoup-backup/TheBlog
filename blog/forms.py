from .models import Comment
from django import forms
from markdownx.fields import MarkdownxFormField

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')

class PostForm(forms.Form):
    postContent = MarkdownxFormField()