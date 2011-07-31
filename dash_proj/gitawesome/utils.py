import time

from django.contrib.auth.models import User
from django.db.models.aggregates import Sum

import git
import simplejson

from lib import github

from gitawesome.models import Commit, Project, Profile


GITHUB_REPO_BASE = 'https://github.com/%s/%s/'

def import_commits(user, project_name, sha=None):
    """
    Import commits starting at sha for give repo.
    """
    project_url = GITHUB_REPO_BASE % (user, project_name)
    if sha:
        project_url = '%s?sha=%s' % (project_url, sha)
    project, _ = Project.objects.get_or_create(url=project_url,
            defaults={'name': project_name})
    commits = github.get_commits(user, project_name)
    profiles_by_author = dict()
    for commit in commits:
        try:
            author = commit['author']['login']
        except TypeError:
            # user not on github, skip commit
            continue
        if author not in profiles_by_author:
            name = commit['commit']['author']['name'].split()
            user, _ = User.objects.get_or_create(username=author, defaults={
                'email': commit['commit']['author']['email'],
                'first_name': name[0],
                'last_name': name[-1],
            })
            user.profile.avatar_url = commit['author']['avatar_url']
            user.profile.save()
            profiles_by_author[author] = user.profile

        sha = commit['sha']
        commit, _ = Commit.objects.get_or_create(project=project, sha=sha,
                defaults={'user': profiles_by_author[author].user})
        # TODO: inspect repo to get changeset size to determine yards
        commit.yards = 1
        commit.save()
        print "*** [DEBUG] imported commit", sha
    return commits

def calculate_points(profile):
    """
    Calculate points for given user.
    """
    profile.yards = Commit.objects.filter(user=profile.user).aggregate(total=Sum('yards')).get('total')
    profile.save()

def get_commit_info(commit):
    fields = (
        'hexsha',
        'stats.total',
        'author.name',
        'author.email',
        'committed_date',
    )
    def _getattr(obj, name, default):
        attrs = name.split('.')
        for a in attrs:
            try:
                obj = getattr(obj, a)
            except AttributeError:
                return default
        return obj
    return dict((f,_getattr(commit, f, '')) for f in fields)

def import_contributors(username, project_name):
    #contributors = github.get_contributors(username, project_name)
    contributors = simplejson.loads(open('contributors.json').read())
    for c in contributors:
        user, created = User.objects.get_or_create(username=c['login'])
        if created:
            # fetch user and update user details
            print "*** [DEBUG] getting github user", c['login']
            time.sleep(2) # ratelimit
            github_user = github.get_user(c['login'])
            if not github_user.get('email'):
                continue
            user.email = github_user['email']
            user.save()
            user.profile.avatar_url = github_user['avatar_url']
            user.profile.save()
    print "*** [DEBUG] imported %d users" % len(contributors)

def import_from_repo(username, project_name):
    COMMITS_TO_SCORE = 1000
    import_contributors(username, project_name)
    project_url = GITHUB_REPO_BASE % (username, project_name)
    project, _ = Project.objects.get_or_create(url=project_url,
            defaults={'name': project_name})
    repo = git.Repo('gunicorn')
    commits = repo.iter_commits('master', max_count=COMMITS_TO_SCORE)
    imported_count = 0
    users_by_email = dict()
    for commit_info in commits:
        commit_info = get_commit_info(commit_info)
        email = commit_info['author.email']
        sha = commit_info['hexsha']
        if email not in users_by_email:
            try:
                users_by_email[email] = User.objects.get(email=email)
            except User.DoesNotExist:
                # user not in github, skip commit
                continue
        commit, _ = Commit.objects.get_or_create(project=project, sha=sha,
                defaults={'user': users_by_email[email]})
        def _yards_from_commit(commit_info):
            return commit_info['stats.total']['lines']
        commit.yards = _yards_from_commit(commit_info)
        imported_count +=1
        commit.save()
        #print "*** [DEBUG] imported commit", sha
    print "*** [DEBUG] imported %d commits" % imported_count

#import_from_repo('benoitc', 'gunicorn')
for p in Profile.objects.filter(user__is_active=True):
    calculate_points(p)
