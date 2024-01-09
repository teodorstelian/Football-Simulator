from django.contrib import admin
from .models import Team, Country, Player


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'skill', 'country', 'logo']

admin.site.register(Team, TeamAdmin)

class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'flag']

admin.site.register(Country, CountryAdmin)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'skill', 'country', 'team', 'photo']

admin.site.register(Player, PlayerAdmin)