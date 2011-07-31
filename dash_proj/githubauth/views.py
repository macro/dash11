import cgi
import urllib
import urllib2

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


GITHUB_REQUEST_TOKEN_URL = 'https://github.com/login/oauth/authorize'
GITHUB_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'

def github_login(request):
    url = '%s?%s' % (GITHUB_REQUEST_TOKEN_URL,
            urllib.urlencode({
                'client_id': settings.GITHUB_CLIENT_ID,
                'redirect_url': request.build_absolute_uri(reverse('github_login_return')),
                }))
    return HttpResponseRedirect(url)

def github_login_return(request):
    try:
        code = request.GET['code']
    except Exception, e:
        print "*** [DEBUG] ", e
        return HttpResponseRedirect(reverse('gitawesome_home'))

    # get access token
    data = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'redirect_url': reverse('github_login_return'),
        'client_secret': settings.GITHUB_SECRET,
        'code': code
    }
    response = urllib2.urlopen(GITHUB_ACCESS_TOKEN_URL, data)

    access_token = dict(cgi.parse_qsl(response))

    print "*** [DEBUG] ", access_token()

    # FIXME: create user
    user = User.objects.create_user(
    )
    user.profile.github_oauth_token = access_token['oauth_token']
    user.profile.github_oauth_secret = access_token['oauth_token_secret']
    user.profile.save()

    user = authenticate(username=access_token['screen_name'],
        password=access_token['oauth_token_secret'])
    login(request, user)
    return HttpResponseRedirect(reverse('gitawesome_home'))

@login_required
def github_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('gitawesome_home'))

