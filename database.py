import sqlite3

from settings import COMPETITIONS_DB
from teams import Team


def create_teams_table(league):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()
    query = '''CREATE TABLE IF NOT EXISTS {} (name TEXT, matches_played INTEGER, wins INTEGER, draws INTEGER, 
    losses INTEGER, points INTEGER, goals_scored INTEGER, goals_against INTEGER)'''.format(league)
    c.execute(query)
    conn.commit()
    conn.close()


def insert_team(team, league):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()
    query = f"INSERT INTO {league} VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    c.execute(query, (
        team.name, team.matches_played, team.wins, team.draws, team.losses, team.points, team.goals_scored,
        team.goals_against
    ))
    conn.commit()
    conn.close()


def update_team(team, league):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()
    query = f"UPDATE {league} SET matches_played=?, wins=?, draws=?, losses=?, points=?, " \
            f"goals_scored=?, goals_against=? WHERE name=?"
    c.execute(query, (team.matches_played, team.wins, team.draws, team.losses, team.points, team.goals_scored,
                      team.goals_against, team.name))
    conn.commit()
    conn.close()


def get_teams(league):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()
    query = f"SELECT * FROM {league}"
    c.execute(query)
    teams_data = c.fetchall()
    conn.close()
    teams = []
    for data in teams_data:
        team = Team(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        teams.append(team)
    return teams


def get_best_teams(league):
    number = input("Select number of best teams:")
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()

    # Query for best teams by points
    query = f"SELECT name, points FROM {league} ORDER BY points DESC LIMIT {number}"
    c.execute(query)
    best_teams = c.fetchall()

    conn.close()

    print(f"{league}'s Best Teams:")
    for team in best_teams:
        print(f"Team: {team[0]}, Points: {team[1]}")
