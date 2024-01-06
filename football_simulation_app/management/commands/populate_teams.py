# football_simulation_app/management/commands/populate_teams.py
from django.core.management.base import BaseCommand
from football_simulation_app.models import Team
from src.teams_data import *

class Command(BaseCommand):
    help = 'Populate initial teams data'

    def handle(self, *args, **options):

        self.create_team(ENG_TEAMS, "England")
        self.create_team(ESP_TEAMS, "Spain")
        self.create_team(GER_TEAMS, "Germany")
        self.create_team(ITA_TEAMS, "Italy")
        self.create_team(FRA_TEAMS, "France")
        self.create_team(NED_TEAMS, "Netherlands")
        self.create_team(POR_TEAMS, "Portugal")
        self.create_team(BEL_TEAMS, "Belgium")
        self.create_team(SCO_TEAMS, "Scotland")
        self.create_team(AUS_TEAMS, "Austria")


    def create_team(self, teams, country):
        for name, skill in teams:
            team, created = Team.objects.get_or_create(
                name=name,
                defaults={
                    "skill": skill,
                    "country": country,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created team: {team.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Team already exists: {team.name}'))