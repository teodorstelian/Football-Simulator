import sqlite3

from teams import Team


def create_teams_table(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS teams (name TEXT, matches_played INTEGER, wins INTEGER, draws INTEGER, 
    losses INTEGER, points INTEGER, goals_scored INTEGER, goals_against INTEGER)''')
    conn.commit()
    conn.close()


def insert_team(team, database):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
        team.name, team.matches_played, team.wins, team.draws, team.losses, team.points, team.goals_scored,
        team.goals_against))
    conn.commit()
    conn.close()


def update_team(team, database):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("UPDATE teams SET matches_played=?, wins=?, draws=?, losses=?, points=?, goals_scored=?, goals_against=? "
              "WHERE name=?", (team.matches_played, team.wins, team.draws, team.losses, team.points, team.goals_scored,
                               team.goals_against, team.name))
    conn.commit()
    conn.close()


def get_teams(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT * FROM teams")
    teams_data = c.fetchall()
    conn.close()
    teams = []
    for data in teams_data:
        team = Team(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        teams.append(team)
    return teams
