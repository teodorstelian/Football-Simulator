from django.contrib import admin
from .models import Team, LeagueTeam, GeneralTeam

class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'skill', 'country', 'logo']

admin.site.register(Team)
admin.site.register(LeagueTeam)
admin.site.register(GeneralTeam)