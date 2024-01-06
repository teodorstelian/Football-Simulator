from django.contrib import admin
from .models import Team, LeagueTeam, GeneralTeam

admin.site.register(Team)
admin.site.register(LeagueTeam)
admin.site.register(GeneralTeam)