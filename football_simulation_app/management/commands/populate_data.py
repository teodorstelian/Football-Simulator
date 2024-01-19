from django.core.management.base import BaseCommand
from football_simulation_app.models import Team, Country, Player
from django.contrib.auth.models import User
from football_simulation_app.management.initial_data import *

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
    if "GK" not in main:
        rat["GK"] = 40
    return rat

class Command(BaseCommand):
    help = 'Populate initial data'

    def handle(self, *args, **options):

        self.create_super_admin()
        self.create_countries()
        self.create_teams(ENG_TEAMS, "England")
        self.create_teams(ESP_TEAMS, "Spain")
        # self.create_team(GER_TEAMS, "Germany")
        # self.create_team(ITA_TEAMS, "Italy")
        # self.create_team(FRA_TEAMS, "France")
        # self.create_team(NED_TEAMS, "Netherlands")
        # self.create_team(POR_TEAMS, "Portugal")
        # self.create_team(BEL_TEAMS, "Belgium")
        # self.create_team(SCO_TEAMS, "Scotland")
        # self.create_team(AUS_TEAMS, "Austria")
        self.create_players()

    def create_teams(self, teams, country_name):
        country, created = Country.objects.get_or_create(name=country_name)
        for name in teams:
            team, created = Team.objects.get_or_create(
                name=name,
                defaults={
                    "country": country,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created team: {team.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Team already exists: {team.name}'))
                team.save()

    def create_players(self):
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

    def create_countries(self):
        for country_name, europe_data in COUNTRIES.items():
            country, created = Country.objects.get_or_create(
                name=country_name,
                defaults={
                    "ucl_places": europe_data["ucl"],
                    "uel_places": europe_data["uel"],
                    "uecl_places": europe_data["uecl"],
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created country: {country.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Country already exists: {country.name}'))

    def create_super_admin(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser "admin" already exists'))
