import sqlite3

import settings
from settings import COMPETITIONS_DB
from team import Team


def create_teams_table(league):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()
    query = f"""
    CREATE TABLE IF NOT EXISTS {league} (
        name TEXT,
        matches_played INTEGER,
        wins INTEGER,
        draws INTEGER,
        losses INTEGER,
        points INTEGER,
        goals_scored INTEGER,
        goals_against INTEGER,
        first_place INTEGER DEFAULT 0,
        second_place INTEGER DEFAULT 0,
        third_place INTEGER DEFAULT 0
    )
    """
    c.execute(query)
    try:
        c.execute(f"ALTER TABLE {league} ADD COLUMN first_place INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        print(f"Column 'first_place' already exists in the {league} table.")

    try:
        c.execute(f"ALTER TABLE {league} ADD COLUMN second_place INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        print(f"Column 'second_place' already exists in the {league} table.")

    try:
        c.execute(f"ALTER TABLE {league} ADD COLUMN third_place INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        print(f"Column 'third_place' already exists in the {league} table.")

    conn.commit()
    conn.close()


def insert_team(team, league):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()
    query = f"""
    INSERT INTO {league} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    c.execute(query, (
        team.name,
        team.matches_played,
        team.wins,
        team.draws,
        team.losses,
        team.points,
        team.goals_scored,
        team.goals_against,
        team.first_place,
        team.second_place,
        team.third_place
    ))
    conn.commit()
    conn.close()


def update_team(team, league):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()
    query = f"""
    UPDATE {league}
    SET matches_played = ?,
        wins = ?,
        draws = ?,
        losses = ?,
        points = ?,
        goals_scored = ?,
        goals_against = ?,
        first_place = ?,
        second_place = ?,
        third_place = ?
    WHERE name = ?
    """
    c.execute(query, (
        team.matches_played,
        team.wins,
        team.draws,
        team.losses,
        team.points,
        team.goals_scored,
        team.goals_against,
        team.first_place,
        team.second_place,
        team.third_place,
        team.name
    ))
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


def get_teams(league=None, european_cup=None, rounds=None):
    """
    Get teams from the league or European competition.
    Allows filtering by specific competition (e.g., UCL) and optional rounds (e.g., 'Round 1', 'Round 2').

    :param league: League name to fetch teams from its table.
    :param european_cup: European competition (e.g., 'UCL', 'UEL', 'UECL').
    :param rounds: List of stages to include (e.g., ['Round 1', 'Round 2']).
    :return: List of Team objects.
    """
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()

    if league:
        query = f"SELECT * FROM {league}"
    elif european_cup:
        if rounds:
            # Filter by multiple rounds (e.g., Round 1 and Round 2)
            rounds_condition = " OR ".join([f"europe LIKE '%- {cur_round}'" for cur_round in rounds])
            query = f"SELECT * FROM {settings.GENERAL_TABLE} WHERE europe LIKE '{european_cup}%' AND ({rounds_condition})"
        else:
            # Include all teams for the competition
            query = f"SELECT * FROM {settings.GENERAL_TABLE} WHERE europe LIKE '{european_cup}%'"
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

        if european_cup:  # Fetch league stats if filtering for Europe
            league_query = f"SELECT * FROM {country} WHERE name = '{team_name}'"
            c.execute(league_query)
            team_stats = c.fetchone()
            name, matches, wins, draws, losses, points, scored, against, first_place, second_place, third_place = team_stats
        elif league:
            name, matches, wins, draws, losses, points, scored, against, first_place, second_place, third_place = data

        # Creating a new Team object with additional attributes (first_place, second_place, third_place)
        team = Team(
            name=name, country=country, skill=skill, matches=matches, wins=wins, draws=draws,
            losses=losses, points=points, scored=scored, against=against, league_titles=titles,
            cup_titles=cups, europe=europe, ucl=ucl, uel=uel, uecl=uecl,
            first_place=first_place, second_place=second_place, third_place=third_place
        )
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

def get_competition_winners_from_db(competition_name):
    """
    Fetches teams with the most wins for a specific competition from the GENERAL_TABLE.

    :param competition_name: Name of the competition (e.g., 'league_titles', 'cup_titles', 'ucl', 'uel', 'uecl').
    :return: List of tuples containing team names and their number of titles, descending by wins.
    """
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()

    # Map competition name to the appropriate field in GENERAL_TABLE
    valid_competitions = {
        "league_titles": "league_titles",
        "cup_titles": "cup_titles",
        "ucl": "ucl",
        "uel": "uel",
        "uecl": "uecl"
    }

    competition_field = valid_competitions.get(competition_name.lower())
    if not competition_field:
        print(f"Invalid competition name: {competition_name}")
        conn.close()
        return []

    # Query to fetch the winners sorted by the specified competition field
    query = f"""
        SELECT name, {competition_field}
        FROM {settings.GENERAL_TABLE}
        WHERE {competition_field} > 0
        ORDER BY {competition_field} DESC
    """
    c.execute(query)
    results = c.fetchall()
    conn.close()
    return results

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

def create_european_competitions_table(competition):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()

    # Replace spaces with underscores for table names
    competition_table = competition.replace(" ","")

    query = f'''CREATE TABLE IF NOT EXISTS {competition_table} (
           team_name TEXT,
           appearances INTEGER DEFAULT 0,
           finals INTEGER DEFAULT 0,
           wins INTEGER DEFAULT 0
       )'''
    c.execute(query)
    conn.commit()
    conn.close()

def update_european_competition_appereances(team_name, competition):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()

    # Replace spaces with underscores for table names
    competition_table = competition.replace(" ", "")

    # Check if the team already exists in the table
    c.execute(f"SELECT appearances FROM {competition_table} WHERE team_name=?", (team_name,))
    row = c.fetchone()

    if row is None:  # Insert new row if the team doesn't exist
        appearances = 1
        c.execute(f"INSERT INTO {competition_table} VALUES (?, ?, ?, ?)", (team_name, appearances, 0, 0))
    else:  # Update appearances and wins if the team already exists
        appearances = row[0]
        appearances += 1
        c.execute(f"UPDATE {competition_table} SET appearances=? WHERE team_name=?",
                  (appearances, team_name))

    conn.commit()
    conn.close()


def update_european_competition_round_team(team_name, competition, round):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()

    # Replace spaces with underscores for table names
    competition_table = competition.replace(" ", "")

    # Check if the team already exists in the table
    c.execute(f"SELECT wins, finals FROM {competition_table} WHERE team_name=?", (team_name,))
    row = c.fetchone()

    wins, finals = row
    if round == "winner":
        wins += 1
    elif round == "finals":
        finals += 1
    c.execute(f"UPDATE {competition_table} SET finals=?, wins=? WHERE team_name=?",
              (finals, wins, team_name))

    conn.commit()
    conn.close()

def get_european_competition_stats(competition):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()

    # Replace spaces with underscores for table names
    competition_table = competition.replace(" ","")

    query = f"SELECT * FROM {competition_table} ORDER BY wins DESC"
    c.execute(query)
    stats = c.fetchall()
    conn.close()
    return stats
