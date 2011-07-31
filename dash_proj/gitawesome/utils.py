import os
from datetime import datetime
import time

from dateutil import parser as date_parser
import git

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum

from lib import github

from gitawesome.models import Commit, Project


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
        commit.points = 1
        commit.save()
        print "*** [DEBUG] imported commit", sha
    return commits

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

def strip_encode(s):
    return str.strip((s or '').encode('utf-8'))

def import_contributors(username, project_name):
    contributors = sorted(github.get_contributors(username, project_name),
        key=lambda x: x.get('contributions', 0), reverse=True)[:20]
    profiles = list()
    for c in contributors:
        user, created = User.objects.get_or_create(username=c['login'])
        if created:
            # fetch user and update user details
            print "*** [DEBUG] getting github user", c['login']
            time.sleep(2) # ratelimit
            github_user = github.get_user(c['login'])
            if not github_user.get('email'):
                continue
            try:
                parts = github_user['name'].split()
                first, last = parts[0], parts[-1]
            except:
                first = github_user['name']
                last = ''
            user.first_name = strip_encode(first)
            user.last_name = strip_encode(last)
            user.email = strip_encode(github_user['email'])
            user.save()
            user.profile.avatar_url = strip_encode(github_user['avatar_url'])
            user.profile.followers = github_user['followers']
            user.profile.following = github_user['following']
            user.profile.gists = github_user['public_gists']
            user.profile.repos = github_user['public_repos']
            user.profile.location = strip_encode(github_user['location'])
            user.profile.company = strip_encode(github_user['company'])
            user.profile.blog = strip_encode(github_user['blog'])
            user.profile.date_joined = date_parser.parse(github_user['created_at'])
            user.profile.save()
        profiles.append(user.profile)
    print "*** [DEBUG] imported %d users" % len(contributors)
    return profiles

def calculate_points(profile):
    """
    Calculate points for given user.
    """
    profile.points = Commit.objects.filter(
            user=profile.user).aggregate(total=Sum('points')).get('total')
    profile.save()

def import_and_analyze_repo(username, project_name):
    COMMITS_TO_SCORE = 10000
    profiles = import_contributors(username, project_name)
    project_url = GITHUB_REPO_BASE % (username, project_name)
    project, _ = Project.objects.get_or_create(url=project_url,
            defaults={'name': project_name})
    path = os.path.join(settings.GIT_REPO_ROOT, project_name)
    try:
        # check if repo exists
        git.Repo().pull(project_url, 'refs/heads/master:refs/heads/origin')
        repo = git.Repo(path)
    except Exception:
        # otherwise, clone it
        repo = git.Repo().clone_from(project_url, path)
    commits = repo.iter_commits('master', max_count=COMMITS_TO_SCORE)
    imported_count = 0
    users_by_email = dict([(profile.user.email, profile.user)
            for profile in profiles])
    print "*** [DEBUG] ", users_by_email.keys()
    for commit_info in commits:
        commit_info = get_commit_info(commit_info)
        email = commit_info['author.email']
        if not email or email not in users_by_email:
            print "*** [DEBUG] skipping", email
            continue
        sha = commit_info['hexsha']
        timestamp = datetime.utcfromtimestamp(float(
                    commit_info['committed_date']))
        commit, _ = Commit.objects.get_or_create(project=project, sha=sha,
                defaults={'user': users_by_email[email], 'timestamp': timestamp})
        def _points_from_commit(commit_info):
            return commit_info['stats.total']['lines']
        commit.points = _points_from_commit(commit_info)
        commit.save()
        imported_count +=1
        #print "*** [DEBUG] imported commit", sha

    for p in profiles:
        calculate_points(p)
    print "*** [DEBUG] imported %d commits" % imported_count

def get_github_repo_url(username, project_name):
    assert username is not None
    assert project_name is not None

    return GITHUB_REPO_BASE % (username, project_name)
