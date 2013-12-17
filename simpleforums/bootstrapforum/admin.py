__author__ = 'dmitriydmitrienko'
from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    search_fields = ['title']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created', 'pic')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)