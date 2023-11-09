from .models import BlogModel
from django import forms
from markdownx.fields import MarkdownxFormField


class PostForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['title', 'content']
