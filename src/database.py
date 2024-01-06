import sqlite3

from src import settings
from src.settings import COMPETITIONS_DB
from src.team import Team


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
    (name TEXT, country TEXT, skill INTEGER, league_titles INTEGER, cup_titles INTEGER, 
    ucl INTEGER, uel INTEGER, uecl INTEGER, europe TEXT) '''
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
                f"(name, country, skill, league_titles, cup_titles, ucl, uel, uecl, europe) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        c.execute(query, (team.name, team.country, team.skill, team.league_titles, team.cup_titles, team.ucl, team.uel, team.uecl, team.europe))
    else:  # Team name exists, update the matching row
        query = f"UPDATE {settings.GENERAL_TABLE} " \
                f"SET country=?, skill=?, league_titles=?, cup_titles=?, ucl=?, uel=?, uecl=?, europe=? WHERE name=?"
        c.execute(query, (team.country, team.skill, team.league_titles, team.cup_titles, team.ucl, team.uel, team.uecl, team.europe, team.name))

    conn.commit()
    conn.close()


def get_teams(league=None, european_cup=None):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()
    if league:
        query = f"SELECT * FROM {league}"
    elif european_cup:
        query = f"SELECT * FROM {settings.GENERAL_TABLE} where europe='{european_cup}'"
    else:
        return
    c.execute(query)
    teams_data = c.fetchall()
    teams = []
    for data in teams_data:
        team_name = data[0]
        team_query = f"SELECT * FROM {settings.GENERAL_TABLE} WHERE name = '{team_name}'"
        c.execute(team_query)
        team_attrib = c.fetchone()
        name, country, skill, titles, cups, ucl, uel, uecl, europe = team_attrib
        if european_cup:
            league_query = f"SELECT * FROM {country} WHERE name = '{team_name}'"
            c.execute(league_query)
            team_stats = c.fetchone()
            name, matches, wins, draws, losses, points, scored, against = team_stats
        elif league:
            name, matches, wins, draws, losses, points, scored, against = data
        team = Team(name=name, country=country, skill=skill, matches=matches, wins=wins, draws=draws,
                    losses=losses, points=points, scored=scored, against=against, league_titles=titles,
                    cup_titles=cups, europe=europe, ucl=ucl, uel=uel, uecl=uecl)
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

def generate_teams_table(league, teams_obj):
    create_teams_table(league)  # Create the teams table if it doesn't exist

    cur_teams = get_teams(league=league)  # Retrieve teams from the database

    if len(cur_teams) == 0:
        for team in teams_obj:
            insert_team(team, league)
        cur_teams = teams_obj

    return cur_teams

def check_team_stats(team, league):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()

    # Get info from General Table
    c.execute(f"SELECT * FROM {settings.GENERAL_TABLE} WHERE name=?", (team.name,))
    general = c.fetchone()
    # Get info from League Table
    c.execute(f"SELECT * FROM {league} WHERE name=?", (team.name,))
    league = c.fetchone()

    if general and league:
        # Access the column values from General table
        name, country, skill, league_titles, cup_titles, ucl, uel, uecl, europe = general
        # Access the column values from League table
        name, matches, wins, draws, losses, points, goals_scored, goals_against = league

        # Print the values
        print("Name:", name)
        print("Country:", country)
        print("Skill:", skill)
        print("Matches played:", matches)
        print("Wins:", wins)
        print("Draws:", draws)
        print("Losses:", losses)
        print("Points:", points)
        print("Goals scored:", goals_scored)
        print("Goals against:", goals_against)
        print("League Titles:", league_titles)
        print("Cup Titles:", cup_titles)
        print("UCL:", ucl)
        print("UEL:", uel)
        print("UECL:", uecl)
        print("European Qualification:", europe)

    # Close the connection
    c.close()
    conn.close()
