from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.contrib.auth.views import logout, login

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'githubauth.views.github_login', name='github_login'),
    url(r'^logout/$', 'githubauth.views.github_logout', name='github_logout'),
    url(r'^login/return/$', 'githubauth.views.github_login_return',
        name='github_login_return'),

    (r'^accounts/login/$', login, {}, 'login'),
    (r'^accounts/logout/$', logout, {'next_page': '/'}, 'logout'),

    url(r'^', include('dash_proj.gitawesome.urls')),
)

urlpatterns += staticfiles_urlpatterns()


