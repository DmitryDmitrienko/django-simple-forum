#coding=utf-8
__author__ = 'dmitriydmitrienko'
from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('creates', )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('created', 'post')
        widgets = {
            'body': forms.Textarea(attrs={'class': 'span9'}),
        }