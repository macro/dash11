import urllib2

import simplejson


GITHUB_API = 'https://api.github.com'
GITHUB_REPO_COMMITS = '%s/repos/%%s/%%s/commits' % GITHUB_API

def get_commits(user, project):
    return simplejson.loads(urllib2.urlopen(GITHUB_REPO_COMMITS % (user,
                    project)).read())

