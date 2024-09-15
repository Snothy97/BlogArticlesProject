from django import forms
from .models import BlogArticle, Comment

class BlogArticleForm(forms.ModelForm):
    class Meta:
        model = BlogArticle
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
