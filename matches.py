
def generate_fixtures(teams):
    fixtures = []
    rounds = len(teams) - 1

    for _ in range(rounds):
        round_fixtures = []
        half_round = len(teams) // 2
        for i in range(half_round):
            fixture = (teams[i], teams[-i - 1])
            round_fixtures.append(fixture)
        fixtures.append(round_fixtures)
        teams.insert(1, teams.pop())

    return fixtures

def play_fixture(teams):
    fixtures = generate_fixtures(teams)

    for _, round_fixtures in enumerate(fixtures):
        print(f"Round {_ + 1}:")
        for home, away in round_fixtures:
            home.play_match(away)

def generate_standings(teams):
    print("--- Final Standings ---")
    teams.sort(key=lambda x: (x.points, x.wins, x.goals_scored), reverse=True)

    for i, team in enumerate(teams):
        if i == 0:
            print(f"Winner: {team.name}")
            team.league_titles += 1
            team.europe = "Champions League"
        print(
            f"{i + 1}. {team.name} - {team.points} points - {team.wins} wins - {team.draws} draws - {team.losses} losses"
            f" - {team.goals_scored} scored - {team.goals_against} against")

    return teams
