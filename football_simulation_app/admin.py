from django.contrib import admin
from .models import Team, Country, Player


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'skill', 'country', 'logo']

admin.site.register(Team)
admin.site.register(Country)
admin.site.register(Player)