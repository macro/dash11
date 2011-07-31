from django.contrib import admin

from gitawesome.models import Profile, Project, Commit

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'repos', 'followers', 'following',
            'date_joined', 'company', 'location')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project)
admin.site.register(Commit)
