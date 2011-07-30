from django.contrib import admin

from gitball.models import Profile, Project, Commit


admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Commit)
