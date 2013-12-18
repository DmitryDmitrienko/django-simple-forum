from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.decorators import login_required
from bootstrapforum.views.view import CreateComment, PostListView, PostView, \
    AuthenticateView, CreateUserView, CabinetView, CreatePostView, DeletePostView, UpdatePostView

from .settings import local as settings


admin.autodiscover()

urlpatterns = patterns('',
                       (r'^i18n/', include('django.conf.urls.i18n')),
                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^setlanguage$', 'bootstrapforum.views.view.change_language', name='language'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^(?P<post_id>\d+)/createcomment$', login_required(CreateComment.as_view()),
                           name='createcomment'),
                       url(r'^login$', AuthenticateView.as_view(), name='login'),
                       url(r'^logout$', 'bootstrapforum.views.view.logout', name='logout'),
                       url(r'^createuser$', CreateUserView.as_view(), name='createuser'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns('',
                             url(r'^$', login_required(PostListView.as_view()), name='index'),
                             url(r'^(?P<post_id>\d+)$', login_required(PostView.as_view()), name='post'),
                             url(r'^user/(?P<user_id>\d+)$', login_required(CabinetView.as_view()), name='userview'),
                             url(r'^createpost$', login_required(CreatePostView.as_view()), name='createpost'),
                             url(r'^deletepost/(?P<post_id>\d+)', login_required(DeletePostView.as_view()),
                                 name='deletepost'),
                             url(r'^updatepost/(?P<post_id>\d+)', login_required(UpdatePostView.as_view()),
                                 name='updatepost'),
)

urlpatterns += staticfiles_urlpatterns()
