import sqlite3

import settings
from settings import COMPETITIONS_DB
from classes import Team


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


def create_general_table():
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()
    query = f'''CREATE TABLE IF NOT EXISTS {settings.GENERAL_TABLE} 
    (name TEXT, country TEXT, skill INTEGER, league_titles INTEGER, ucl INTEGER, uel INTEGER, uecl INTEGER) '''
    c.execute(query)
    conn.commit()
    conn.close()


def update_general_table(team):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()

    # Check if the team name already exists in the table
    c.execute(f"SELECT COUNT(*) FROM {settings.GENERAL_TABLE} WHERE name=?", (team.name,))
    count = c.fetchone()[0]

    if count == 0:  # Team name does not exist, insert a new row
        query = f"INSERT INTO {settings.GENERAL_TABLE} " \
                f"(name, country, skill, league_titles, ucl, uel, uecl) VALUES (?, ?, ?, ?, ?, ?, ?)"
        c.execute(query, (team.name, team.country, team.skill, team.league_titles, team.ucl, team.uel, team.uecl))
    else:  # Team name exists, update the matching row
        query = f"UPDATE {settings.GENERAL_TABLE} " \
                f"SET country=?, skill=?, league_titles=?, ucl=?, uel=?, uecl=? WHERE name=?"
        c.execute(query, (team.country, team.skill, team.league_titles, team.ucl, team.uel, team.uecl, team.name))

    conn.commit()
    conn.close()


def get_teams(league):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()
    league_query = f"SELECT * FROM {league}"
    c.execute(league_query)
    teams_data = c.fetchall()
    teams = []
    for data in teams_data:
        team_name = data[0]
        team_query = f"SELECT skill FROM {settings.GENERAL_TABLE} WHERE name = '{team_name}'"
        c.execute(team_query)
        team_skill = c.fetchone()
        team = Team(name=team_name, country=league, skill=team_skill, matches=data[1], wins=data[2], draws=data[3],
                    losses=data[4], points=data[5], scored=data[6], against=data[7])
        teams.append(team)
    conn.close()
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