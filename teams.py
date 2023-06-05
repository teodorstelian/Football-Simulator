import settings
from classes import Team


def teams_england():
    Arsenal = Team(name="Arsenal", country=settings.ENG, skill="90")
    Aston_Villa = Team(name="Aston Villa", country=settings.ENG, skill="70")
    Bournemouth = Team(name="Bournemouth", country=settings.ENG, skill="65")
    Brentford = Team(name="Brentford", country=settings.ENG, skill="60")
    all_teams_obj = [Arsenal, Aston_Villa, Bournemouth, Brentford]
    all_teams_names = [Arsenal.name, Aston_Villa.name, Bournemouth.name, Brentford.name]
    return all_teams_obj, all_teams_names


def teams_spain():
    return teams_england()


def teams_germany():
    return teams_england()


def teams_italy():
    return teams_england()


def teams_france():
    return teams_england()
