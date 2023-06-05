import settings
from classes import Team


def teams_england():
    all_teams_obj = []
    all_teams_names = []
    for team, skill in settings.ENG_TEAMS:
        new_team = Team(name=team, country=settings.ENG, skill=skill)
        all_teams_obj.append(new_team)
        all_teams_names += new_team.name
    # Arsenal = Team(name="Arsenal", country=settings.ENG, skill="90")
    # Aston_Villa = Team(name="Aston Villa", country=settings.ENG, skill="70")
    # Bournemouth = Team(name="Bournemouth", country=settings.ENG, skill="65")
    # Brentford = Team(name="Brentford", country=settings.ENG, skill="60")
    # all_teams_obj = [Arsenal, Aston_Villa, Bournemouth, Brentford]
    # all_teams_names = [Arsenal.name, Aston_Villa.name, Bournemouth.name, Brentford.name]
    return all_teams_obj, all_teams_names


def teams_spain():
    return teams_england()


def teams_germany():
    return teams_england()


def teams_italy():
    return teams_england()


def teams_france():
    return teams_england()
