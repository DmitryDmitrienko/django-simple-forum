__author__ = 'dmitriydmitrienko'
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from .models import Post, Comment
from .forms import UserForumForm, CreateUserForumForm


class UserAdminForum(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'language', 'avatar')
    add_form = CreateUserForumForm
    form = UserForumForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'avatar', 'language')}
        ),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_("Profile"), {'fields': ('language', 'avatar')}),
    )


class PostAdmin(admin.ModelAdmin):
    search_fields = ['title']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'created')


User = get_user_model()
admin.site.register(User, UserAdminForum)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)