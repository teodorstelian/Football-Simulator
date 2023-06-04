import random
import sqlite3

from teams import Team


def create_teams_table():
    conn = sqlite3.connect("football.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS teams
                 (name TEXT, matches_played INTEGER, wins INTEGER, draws INTEGER, losses INTEGER, points INTEGER, goals_scored INTEGER, goals_against INTEGER)''')
    conn.commit()
    conn.close()


def insert_team(team):
    conn = sqlite3.connect("football.db")
    c = conn.cursor()
    c.execute("INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (team.name, team.matches_played, team.wins, team.draws, team.losses, team.points, team.goals_scored, team.goals_against))
    conn.commit()
    conn.close()


def get_teams():
    conn = sqlite3.connect("football.db")
    c = conn.cursor()
    c.execute("SELECT * FROM teams")
    teams_data = c.fetchall()
    conn.close()
    teams = []
    for data in teams_data:
        team = Team(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        teams.append(team)
    return teams


create_teams_table()  # Create the teams table if it doesn't exist

teams = get_teams()  # Retrieve teams from the database

if len(teams) == 0:
    teams = [
        Team("Team A"),
        Team("Team B"),
        Team("Team C"),
        Team("Team D"),
    ]

fixtures = [(teams[i], teams[j]) for i in range(len(teams)) for j in range(i + 1, len(teams))]

for round in range(1, len(teams)):
    print(f"--- Round {round} ---")
    random.shuffle(fixtures)
    for home_team, away_team in fixtures:
        home_team.play_match(away_team)

for team in teams:
    insert_team(team)  # Update team data in the database

print("--- Final Standings ---")
teams = get_teams()  # Retrieve teams with updated data from the database
teams.sort(key=lambda x: (x.points, x.wins, x.goals_scored), reverse=True)
for i, team in enumerate(teams):
    print(
        f"{i + 1}. {team.name} - {team.points} points - {team.wins} wins - {team.draws} draws - {team.losses} losses"
        f" - {team.goals_scored} scored - {team.goals_against} against")
