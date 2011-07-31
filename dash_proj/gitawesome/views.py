import urllib
import urlparse
from collections import defaultdict
import itertools, operator

from django.core.cache import cache
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify

from gitawesome.models import Project, Profile, Commit
from gitawesome.forms import RepoForm
from gitawesome.tasks import analyze_repo


def home(request):
    context = {
    }
    return render_to_response('gitawesome/home.html', context,
        context_instance=RequestContext(request))

def repo(request):
    repo_form = RepoForm()
    if request.method == 'POST':
        repo_form = RepoForm(request.POST)
        if repo_form.is_valid():
            # queue repo analysis
            url = repo_form.cleaned_data['repo_url']
            parts = urlparse.urlsplit(url)
            username, project_name = filter(None, parts[2].split('/'))
            User.objects.get_or_create(username=username)
            Project.objects.get_or_create(name=project_name,
                    url='https://github.com/%s/%s/' % (username, project_name))
            analyze_repo.delay(username, project_name)
            return HttpResponseRedirect('%s?%s' % (
                        reverse('gitawesome_repo_queued'), urllib.urlencode({
                            'username': username,
                            'project_name': project_name,
                        })))
    context = {
        'repo_form': repo_form,
    }
    return render_to_response('gitawesome/repo.html', context,
        context_instance=RequestContext(request))

def repo_queued(request):
    username = request.GET.get('username')
    project_name = request.GET.get('project_name')
    context = {
        'username': username,
        'project_name': project_name,
    }
    return render_to_response('gitawesome/repo_queued.html', context,
        context_instance=RequestContext(request))



def user(request, username):
    profile = get_object_or_404(Profile, slug=slugify(username))
    if (request.user.is_authenticated() and
            profile.user.username == request.user.username):
        # show dashboard
        #return HttpResponseRedirect(reverse('gitawesome_dashboard',
        #args=(request.user.username,)))
        pass
    commits_by_project = defaultdict(list)
    for c in Commit.objects.filter(
            user=profile.user).order_by('project__id'):
        commits_by_project[c.project].append(c)
    context = {
        'profile': profile,
        'commits_by_project': commits_by_project.iteritems(),
    }
    return render_to_response('gitawesome/user.html', context,
        context_instance=RequestContext(request))

def project(request, username, project_name):
    key = 'project-%s-%s' % (username, project_name)
    context = cache.get(key)
    if context is None:
        profile = get_object_or_404(Profile, slug=slugify(username))
        project = get_object_or_404(Project, slug=slugify(project_name))
        commits_by_user = defaultdict(list)
        for c in project.commit_set.all():
            commits_by_user[c.user].append(c)
        commits = sorted([(sum(c.points for c in commits), user)
            for user,commits in commits_by_user.iteritems()], reverse=True)
        context = {
            'profile': profile,
            'project': project,
            'commits': commits,
        }
        cache.set(key, context, 3600)
    return render_to_response('gitawesome/project.html', context,
        context_instance=RequestContext(request))

