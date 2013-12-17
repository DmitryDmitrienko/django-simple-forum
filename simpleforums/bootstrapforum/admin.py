__author__ = 'dmitriydmitrienko'
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Post, Comment, UserForum


class UserAdminForum(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'language', 'avatar')

    def get_fieldsets(self, request, obj=None):
        field = list(super(UserAdminForum, self).get_fieldsets(request, obj))
        field.append(
            (_("Profile"), {'fields': ('language', 'avatar')}),
        )
        return field


class PostAdmin(admin.ModelAdmin):
    search_fields = ['title']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created', 'pic')


admin.site.register(UserForum, UserAdminForum)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)