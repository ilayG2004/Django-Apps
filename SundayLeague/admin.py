"""
FILE: SundayLeague/admin.py
AUTHOR: Ilay Guler (ilay2004@bu.edu)
DESCRIPTION: Registering data models to admin site so dev's can easily CRUD data.
DATE: 4/17/2026
"""
from django.contrib import admin
from .models import *
# Register sunday league models
admin.site.register(SLProfile)
admin.site.register(League)
admin.site.register(Game)
admin.site.register(Team)
admin.site.register(LeaguePost)
admin.site.register(TeamMember)
admin.site.register(Upvote)
admin.site.register(TeamJoinRequest)
admin.site.register(LeagueJoinRequest)
