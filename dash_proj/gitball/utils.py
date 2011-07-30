from django.contrib.auth.models import User
from django.db.models.aggregates import Sum

from lib import github

from gitball.models import Commit, Project, Profile


GITHUB_REPO_BASE = 'https://github.com/%s/%s/'

def import_commits(user, project_name, sha=None):
    """
    Import commits starting at sha for give repo.
    """
    project_url = GITHUB_REPO_BASE % (user, project_name)
    if sha:
        project_url = '%s?sha=%s' % (project_url, sha)
    print "*** [DEBUG] fetching", project_url
    project, _ = Project.objects.get_or_create(url=project_url,
            defaults={'name': project_name})
    commits = github.get_commits(user, project_name)
    #import simplejson
    #commits = simplejson.loads(open('data/test.json').read())
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

def calculate_points(username):
    """
    Calculate points for given user.
    """
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return
    profile.yards = Commit.objects.filter(user=profile.user).aggregate(total=Sum('yards')).get('total')
    profile.save()

