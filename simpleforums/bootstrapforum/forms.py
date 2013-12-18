#coding=utf-8
__author__ = 'dmitriydmitrienko'
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Post, Comment, UserForum


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


class UserForumForm(forms.ModelForm):
    class Meta:
        model = UserForum


class CreateUserForumForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserForum
        fields = ('avatar', 'language')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(CreateUserForumForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user