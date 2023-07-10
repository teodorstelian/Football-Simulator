from matches import generate_fixtures_cup


def play_european_cup(teams, competition):
    teams_name = [team.name for team in teams]
    print(teams_name)
    generate_fixtures_cup(teams, competition)