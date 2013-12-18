from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from simpleforum.settings.local import LANGUAGES


class UserForum(AbstractUser):
    language = models.CharField(max_length=40, choices=LANGUAGES, default=LANGUAGES[0][1],
                                verbose_name=_('language user'))
    avatar = models.ImageField(upload_to='profile/avatar/%Y/%m/%d/', blank=False, null=True,
                               verbose_name=_("avatar user"), default='profile/user.png')


class Post(models.Model):
    title = models.CharField(max_length=60, verbose_name=_('title post'), help_text=_('title post'))
    body = models.TextField(verbose_name=_('body post'), help_text=_('body of the post'))
    creates = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('post', args=[str(self.id)])

    def __unicode__(self):
        return unicode(self.title)


class Comment(models.Model):
    author = models.ForeignKey(UserForum, verbose_name=_("author post"))
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(verbose_name=_('body comment'), help_text=_('body of the comment'))
    post = models.ForeignKey(Post, related_name='comments')

    def __unicode__(self):
        return u"%s %s" % (self.post, self.body[:60])