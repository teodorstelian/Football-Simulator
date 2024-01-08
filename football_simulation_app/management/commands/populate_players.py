# football_simulation_app/management/commands/populate_players.py
from django.core.management.base import BaseCommand
from football_simulation_app.models import Player, Team, Country
from src.initial_data import PLAYERS  # Import your player data

class Command(BaseCommand):
    help = 'Populate initial players data'

    def handle(self, *args, **options):
        for player_data in PLAYERS:
            player_name, team_name, country_name, skill, main_pos, sec_pos, ter_pos, age = player_data

            country, created = Country.objects.get_or_create(name=country_name)
            team = Team.objects.get(name=team_name)

            player, created = Player.objects.get_or_create(
                name=player_name,
                team=team,
                country=country,
                defaults={
                    "skill": skill,
                    "main_positions": main_pos,
                    "secondary_positions": sec_pos,
                    "tertiary_positions": ter_pos,
                    "age": age,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created player: {player.team.name} - {player.main_positions}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Player already exists: {player.team.name} - {player.main_positions}'))
