from django.core.management.base import BaseCommand
from football_simulation_app.models import Team, Country
from src.initial_data import *

class Command(BaseCommand):
    help = 'Populate initial teams_logo data'

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

    def create_team(self, teams, country_name):
        country, created = Country.objects.get_or_create(name=country_name)
        for name, skill, *rest in teams:
            logo_path = rest[0] if rest else None  # Extract logo_path if provided, else set to None
            team, created = Team.objects.get_or_create(
                name=name,
                defaults={
                    "skill": skill,
                    "country": country,
                }
            )

            if logo_path:
                team.logo.name = logo_path
                team.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created team: {team.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Team already exists: {team.name}'))
