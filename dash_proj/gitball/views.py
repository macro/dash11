import itertools, operator

from django.core.cache import cache
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify

from gitball.models import Project, Profile, Commit


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('gitball_user',
                    args=(request.user.username,)))
    context = {
    }
    return render_to_response('gitball/home.html', context,
        context_instance=RequestContext(request))

def user(request, username):
    profile = get_object_or_404(Profile, slug=slugify(username))
    if (request.user.is_authenticated() and
            profile.user.username == request.user.username):
        # show dashboard
        #return HttpResponseRedirect(reverse('gitball_dashboard',
        #args=(request.user.username,)))
        pass
    context = {
        'profile': profile,
        'commits': Commit.objects.filter(user=profile.user),
    }
    return render_to_response('gitball/user.html', context,
        context_instance=RequestContext(request))

def project(request, username, project_name):
    key = 'project-%s-%s' % (username, project_name)
    context = cache.get(key)
    if context is None:
        profile = get_object_or_404(Profile, slug=slugify(username))
        project = get_object_or_404(Project, slug=slugify(project_name))

        user_commits = itertools.groupby(sorted(project.commit_set.all(),
                    key=operator.attrgetter('user.pk')),
                operator.attrgetter('user'))
        commits_by_user = sorted([(sum(c.yards for c in commits), user)
                for user, commits in user_commits], reverse=True)
        context = {
            'profile': profile,
            'project': project,
            'commits_by_user': commits_by_user,
        }
        cache.set(key, context, 3600)
    return render_to_response('gitball/project.html', context,
        context_instance=RequestContext(request))

