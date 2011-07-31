from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.template.defaultfilters import slugify


class Project(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, blank=True)
    url = models.URLField(verify_exists=False)

    def __unicode__(self):
        return u'%s' % self.name

    def get_github_url(self):
        return self.url


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar_url = models.URLField(verify_exists=False)
    slug = models.SlugField(max_length=256, blank=True)

    # stats
    points = models.IntegerField(default=0)
    passes = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s' % self.user.username

    def get_github_url(self):
        return 'https://github.com/%s/' % self.user.username


class Commit(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    sha = models.CharField(max_length=256)

    points = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s' % self.sha

    def get_github_url(self):
        return '%scommit/%s/' % (self.project.get_github_url(), self.sha)

def on_profile_pre_save(sender, instance, using, **kwargs):
    instance.slug = slugify(instance.user.username)

def on_project_pre_save(sender, instance, using, **kwargs):
    instance.slug = slugify(instance.name)

def on_user_post_save(sender, instance, created, using, **kwargs):
    if created:
        Profile.objects.create(user=instance)

signals.pre_save.connect(on_project_pre_save, sender=Project)
signals.pre_save.connect(on_profile_pre_save, sender=Profile)
signals.post_save.connect(on_user_post_save, sender=User)
