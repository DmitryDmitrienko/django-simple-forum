#coding=utf-8

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from simpleforums.bootstrapforum.models import Post, Comment
from simpleforums.bootstrapforum.forms import CommentForm


class PostListView(ListView):
    template_name = 'index.html'
    http_method_names = ('get', )
    model = Post
    context_object_name = 'posts'


class PostView(DetailView):
    template_name = "post.html"
    http_method_names = ('get', )
    model = Post
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context.update(dict(
            form=CommentForm()
        ))
        return context


class CreateComment(CreateView):
    template_name = "post.html"
    form_class = CommentForm
    pk_url_kwarg = 'id'
    http_method_names = ('post', )
    model = Comment

    def get_success_url(self):
        return reverse('post', args=(self.kwargs['post_id'], ))


    def form_valid(self, form):
        Comment.objects.create(
            post=Post.objects.get(id=self.kwargs['post_id']),
            **form.cleaned_data
        )
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        context = self.get_context_data(**self.kwargs)
        context.update(dict(
            post=Post.objects.get(id=context['post_id']),
            form=form
        ))
        return self.render_to_response(context)


def change_language(request):
    from django.views.i18n import set_language

    r = request.META.get('HTTP_REFERER')
    if request.LANGUAGE_CODE == 'ru':
        r = r.replace('/ru/', '/en/')
    else:
        r = r.replace('/en/', '/ru/')
    set_language(request)
    return HttpResponseRedirect(r)