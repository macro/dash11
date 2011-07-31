from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('gitawesome.views',
    url(r'^$', 'home', name='gitawesome_home'),

    url(r'^(?P<username>\w+)/$', 'user', name='gitawesome_user'),
    url(r'^(?P<username>\w+)/(?P<project_name>\w+)/$', 'project',
        name='gitawesome_project'),
)
