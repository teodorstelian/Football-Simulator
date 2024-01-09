# football_simulation_app/management/commands/populate_players.py
from django.core.management.base import BaseCommand
from football_simulation_app.models import Player, Team, Country
from src.initial_data import PLAYERS, POSITIONS  # Import your player data


def calculate_position_ovr(skill, main, sec, ter):
    rat= {}
    for pos in POSITIONS:
        if pos in main:
            rat[pos] = skill
        elif pos in sec:
            rat[pos] = 0.92 * skill
        elif pos in ter:
            rat[pos] = 0.82 * skill
        else:
            rat[pos] = 0.65 * skill
    return rat


class Command(BaseCommand):
    help = 'Populate initial players data'

    def handle(self, *args, **options):
        for player_data in PLAYERS:
            player_name, team_name, country_name, skill, main_pos, sec_pos, ter_pos, age = player_data

            country, created = Country.objects.get_or_create(name=country_name)
            team = Team.objects.get(name=team_name)

            pos_rat = calculate_position_ovr(skill, main_pos, sec_pos, ter_pos)
            player, created = Player.objects.get_or_create(
                name=player_name,
                team=team,
                country=country,
                defaults={
                    "skill": skill,
                    "main_position": main_pos,
                    "secondary_positions": sec_pos,
                    "tertiary_positions": ter_pos,
                    "age": age,
                    "GK": pos_rat["GK"],
                    "LB": pos_rat["LB"],
                    "CB": pos_rat["CB"],
                    "RB": pos_rat["RB"],
                    "WLB": pos_rat["WLB"],
                    "WRB": pos_rat["WRB"],
                    "CDM": pos_rat["CDM"],
                    "CM": pos_rat["CM"],
                    "CAM": pos_rat["CAM"],
                    "LM": pos_rat["LM"],
                    "RM": pos_rat["RM"],
                    "RW": pos_rat["RW"],
                    "LW": pos_rat["LW"],
                    "ST": pos_rat["ST"],
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created player: {player.name} - {player.main_position}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Player already exists: {player.name} - {player.main_position}'))

