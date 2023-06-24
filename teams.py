import settings
from classes import Team

def get_teams_country(teams, country):
    all_teams_obj = []
    all_teams_names = []
    for team, skill in teams:
        new_team = Team(name=team, country=country, skill=skill)
        all_teams_obj.append(new_team)
        all_teams_names += new_team.name
    return all_teams_obj, all_teams_names

def teams_england():
    return get_teams_country(settings.ENG_TEAMS, settings.ENG)

def teams_spain():
    return get_teams_country(settings.ESP_TEAMS, settings.ESP)


def teams_germany():
    return get_teams_country(settings.GER_TEAMS, settings.GER)


def teams_italy():
    return get_teams_country(settings.ITA_TEAMS, settings.ITA)


def teams_france():
    return get_teams_country(settings.FRA_TEAMS, settings.FRA)
