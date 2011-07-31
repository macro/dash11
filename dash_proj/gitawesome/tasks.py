from celery.decorators import task

from django.db.models.aggregates import Sum

from gitawesome.models import Commit, Profile
from gitawesome.utils import import_and_analyze_repo

@task
def analyze_repo(username, project_name, **kwargs):
    """
    Get contributor info and clone and analyze repo.
    """
    import_and_analyze_repo(username, project_name)

@task
def calculate_points(username, **kwargs):
    """
    Calculate points for given user.
    """
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return
    profile.points = Commit.objects.filter(
            user=profile.user).aggregate(total=Sum('points')).get('total')
    profile.save()


