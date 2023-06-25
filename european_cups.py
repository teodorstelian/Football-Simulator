from matches import generate_fixtures_cup


def champions_league(teams):
    teams_name = [team.name for team in teams]
    print(teams_name)
    generate_fixtures_cup(teams)