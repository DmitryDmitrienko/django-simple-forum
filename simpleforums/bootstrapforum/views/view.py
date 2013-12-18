#coding=utf-8

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import logout_then_login, auth_login
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.views.decorators.http import require_http_methods

from simpleforums.bootstrapforum.models import Post, Comment, UserForum
from simpleforums.bootstrapforum.forms import CommentForm, PostForm
from simpleforum.settings.local import LANGUAGES


def is_admin(user):
    try:
        group, created = Group.objects.get_or_create(name="Admin")
        #TODO: придумать что-то получше для определения принадлежности группе
        return user in group.user_set.all()
    except Exception:
        return False


class PostListView(ListView):
    template_name = 'index.html'
    http_method_names = ('get', )
    model = Post
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context.update(dict(
            is_admin=is_admin(self.request.user)
        ))
        return context


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
        user = self.request.user
        Comment.objects.create(
            post=Post.objects.get(id=self.kwargs['post_id']),
            author=user,
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


@require_http_methods(["POST"])
def change_language(request):
    from django.views.i18n import set_language

    r = request.META.get('HTTP_REFERER')
    set_language(request)
    if r:
        if request.LANGUAGE_CODE == 'ru':

            r = r.replace('/ru/', '/en/')
        else:
            r = r.replace('/en/', '/ru/')
        import json

        return HttpResponse(
            json.dumps({
                'success': 'success',
                'url': r,
            })
        )
    else:
        return redirect(reverse('index'))


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
            g = Group.objects.get_or_create(name='Users')
            g.user_set.add(u)
            g.save()
            u.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(self.request, u)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(reverse('login'))


class CabinetView(DetailView):
    template_name = "user.html"
    model = UserForum
    http_method_names = ('get',)
    pk_url_kwarg = "user_id"
    context_object_name = "user_forum"


class CreatePostView(CreateView):
    template_name = "createpost.html"
    model = Post
    form_class = PostForm

    def get_success_url(self):
        if self.object:
            return self.object
        else:
            return reverse('createpost')


    def form_valid(self, form):
        user = self.request.user
        if user.is_authenticated():
            self.object = self.model(
                author=user,
                **form.cleaned_data
            )
            self.object.save()
        return redirect(self.get_success_url())


class DeletePostView(DeleteView):
    template_name = "deletepost.html"
    model = Post
    pk_url_kwarg = 'post_id'
    http_method_names = ("post", "get", "delete")

    def get_success_url(self):
        return reverse('index')

    def post(self, request, *args, **kwargs):
        if is_admin(request.user) or request.user == self.get_object().author:
            return super(DeletePostView, self).delete(self.request, *args, **kwargs)
        else:
            return redirect(reverse('index'))

    def get(self, request, *args, **kwargs):
        if is_admin(request.user) or request.user == self.get_object().author:
            return super(DeletePostView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse('index'))


class UpdatePostView(UpdateView):
    template_name = "updatepost.html"
    model = Post
    pk_url_kwarg = "post_id"
    http_method_names = ("post", "get",)
    form_class = PostForm

    def get_success_url(self):
        return reverse("index")

    def post(self, request, *args, **kwargs):
        if is_admin(request.user) or request.user == self.get_object().author:
            return super(UpdatePostView, self).post(request, *args, **kwargs)
        else:
            return redirect(reverse('index'))

    def get(self, request, *args, **kwargs):
        if is_admin(request.user) or request.user == self.get_object().author:
            return super(UpdatePostView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse('index'))