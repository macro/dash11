from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.contrib.auth.views import logout, login


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    (r'^accounts/login/$', login, {}, 'login'),
    (r'^accounts/logout/$', logout, {'next_page': '/'}, 'logout'),

    url(r'^', include('dash_proj.gitball.urls')),
)

urlpatterns += staticfiles_urlpatterns()

