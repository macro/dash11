from django.contrib import admin

from gitawesome.models import Profile, Project, Commit


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'repos', 'followers', 'following',
            'date_joined', 'company', 'location')

class CommitAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'short_hash', 'timestamp', 'points')

    def short_hash(self, obj):
        return obj.sha[:10]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project)
admin.site.register(Commit, CommitAdmin)
