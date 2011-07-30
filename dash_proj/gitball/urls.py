from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('gitball.views',
    url(r'^$', 'home', name='gitball_home'),

    url(r'^(?P<username>\w+)/$', 'user', name='gitball_user'),
    url(r'^(?P<username>\w+)/(?P<project_name>\w+)/$', 'project', name='gitball_project'),
)
