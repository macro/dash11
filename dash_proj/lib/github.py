import urllib2

import simplejson


GITHUB_API = 'https://api.github.com'
GITHUB_REPO_COMMITS = '%s/repos/%%s/%%s/commits' % GITHUB_API
GITHUB_REPO_CONTRIBUTORS = '%s/repos/%%s/%%s/contributors' % GITHUB_API
GITHUB_USER = '%s/users/%%s' % GITHUB_API

def get_commits(user, project):
    return simplejson.loads(urllib2.urlopen(GITHUB_REPO_COMMITS % (user,
                    project)).read())

def get_contributors(user, project):
    return simplejson.loads(urllib2.urlopen(GITHUB_REPO_CONTRIBUTORS % (user,
                    project)).read())

def get_user(user):
    return simplejson.loads(urllib2.urlopen(GITHUB_USER % (user,)).read())

