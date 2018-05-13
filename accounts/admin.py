from django.contrib import admin
from .models import Profile, Team, Comment, Change

admin.site.register(Profile)
admin.site.register(Team)
admin.site.register(Change)
admin.site.register(Comment)

