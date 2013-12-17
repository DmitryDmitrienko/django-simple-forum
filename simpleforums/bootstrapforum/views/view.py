#coding=utf-8

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import logout_then_login, auth_login
from django.shortcuts import redirect
from django.contrib.auth.models import Group

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


class AuthenticateView(FormView):
    form_class = AuthenticationForm
    template_name = "authenticate.html"
    http_method_names = ('post', 'get', )

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        if self.request.GET:
            return redirect(self.request.GET['next'])
        else:
            return super(AuthenticateView, self).form_valid(form)


def logout(request):
    return logout_then_login(request, login_url='/login')


class CreateUserView(CreateView):
    form_class = UserCreationForm
    template_name = "createuser.html"
    http_method_names = ('get', 'post')

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        u = form.save()
        if u:
            g = Group.objects.get(name='Users')
            g.user_set.add(u)
            g.save()
            u.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(self.request, u)
            return HttpResponseRedirect(self.get_success_url())
        else:
            HttpResponseRedirect(reverse('login'))


