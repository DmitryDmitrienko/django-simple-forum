from django.db import models
from django.utils.translation import ugettext_lazy as _


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
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=60, verbose_name=_('author comment'), help_text=_('author of the comment'))
    body = models.TextField(verbose_name=_('body comment'), help_text=_('body of the comment'))
    post = models.ForeignKey(Post, related_name='comments')
    pic = models.ImageField(upload_to='pic/%Y/%m/%d/', verbose_name=_('image author'), help_text=_('image of author'),
                            blank=False)

    def __unicode__(self):
        return u"%s %s" % (self.post, self.body[:60])