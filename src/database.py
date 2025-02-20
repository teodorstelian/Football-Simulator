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
        third_place INTEGER DEFAULT 0,
        cup_finals INTEGER DEFAULT 0,
        cup_wins INTEGER DEFAULT 0
    )
    """
    c.execute(query)

    conn.commit()
    conn.close()


def insert_team(team, league):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()
    query = f"""
    INSERT INTO {league} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        team.third_place,
        team.cup_finals,
        team.cup_wins
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
        third_place = ?,
        cup_finals = ?,
        cup_wins = ?
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
        team.cup_finals,
        team.cup_wins,
        team.name
    ))
    conn.commit()
    conn.close()

def update_team_parameter(team, league, parameter_name, team_parameter):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()
    query = f"""
    UPDATE {league}
    SET {parameter_name} = ?
    WHERE name = ?
    """
    c.execute(query, (
        team_parameter,
        team.name
    ))
    conn.commit()
    conn.close()

def create_general_table():
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()
    query = f"""
    CREATE TABLE IF NOT EXISTS {settings.GENERAL_TABLE} (
        name TEXT,
        country TEXT,
        skill INTEGER,
        league_titles INTEGER DEFAULT 0,
        cup_titles INTEGER DEFAULT 0,
        ucl INTEGER DEFAULT 0,
        uel INTEGER DEFAULT 0,
        uecl INTEGER DEFAULT 0,
        europe TEXT
    )
    """
    c.execute(query)
    conn.commit()
    conn.close()

def update_general_table_with_stats():
    """
    Updates the GENERAL_TABLE with values based on the connected league and European competition tables.
    - League titles (league_titles) come from 'first_place' in their respective league.
    - UCL (or other competition titles) is the 'wins' count from the European competition table.
    """
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()

    # Fetch all teams listed in the GENERAL_TABLE
    c.execute(f"SELECT name, country FROM {settings.GENERAL_TABLE}")
    general_teams = c.fetchall()

    for team_name, country in general_teams:
        # Update the league_titles using 'first_place' from the league table
        league_query = f"SELECT first_place FROM {country} WHERE name = ?"
        c.execute(league_query, (team_name,))
        league_result = c.fetchone()

        if league_result:
            league_titles = league_result[0]
        else:
            league_titles = 0

        update_query = f"""
              UPDATE {settings.GENERAL_TABLE}
              SET league_titles = ?
              WHERE name = ?
              """
        c.execute(update_query, (league_titles, team_name))

        cup_query = f"SELECT cup_wins FROM {country} WHERE name = ?"
        c.execute(cup_query, (team_name,))
        cup_result = c.fetchone()

        if cup_result:
            cup_titles = cup_result[0]
        else:
            cup_titles = 0

        update_query = f"""
                      UPDATE {settings.GENERAL_TABLE}
                      SET cup_titles = ?
                      WHERE name = ?
                      """
        c.execute(update_query, (cup_titles, team_name))

        for competition in [settings.UCL, settings.UEL, settings.UECL]:
            competition_table = competition.replace(" ", "")
            query = f"SELECT wins FROM {competition_table} WHERE team_name = ?"
            c.execute(query, (team_name,))
            result = c.fetchone()

            if result:
                wins = result[0]
            else:
                wins = 0

            if competition == settings.UCL:
                # Update the GENERAL_TABLE with the new stats
                update_query = f"""
                        UPDATE {settings.GENERAL_TABLE}
                        SET ucl = ?
                        WHERE name = ?
                        """
                c.execute(update_query, (wins, team_name))
            elif competition == settings.UEL:
                update_query = f"""
                                 UPDATE {settings.GENERAL_TABLE}
                                 SET uel = ?
                                 WHERE name = ?
                                 """
                c.execute(update_query, (wins, team_name))
            elif competition == settings.UECL:
                update_query = f"""
                                          UPDATE {settings.GENERAL_TABLE}
                                          SET uecl = ?
                                          WHERE name = ?
                                          """
                c.execute(update_query, (wins, team_name))

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
            name, matches, wins, draws, losses, points, scored, against, first_place, second_place, third_place, cup_finals, cup_wins = team_stats
        elif league:
            name, matches, wins, draws, losses, points, scored, against, first_place, second_place, third_place, cup_finals, cup_wins = data

        # Creating a new Team object with additional attributes (cup_finals, cup_wins)
        team = Team(
            name=name, country=country, skill=skill, matches=matches, wins=wins, draws=draws,
            losses=losses, points=points, scored=scored, against=against, first_place=first_place,
            second_place=second_place, third_place=third_place, cup_finals=cup_finals, cup_wins=cup_wins,
            europe=europe
        )
        teams.append(team)

    conn.close()
    return teams


def get_best_teams(league, limit=10):
    """
    Retrieve the best teams from a league table based on specific criteria (e.g., first place, cup wins),
    while displaying all relevant fields for each team.

    :param league: The league table name to query.
    :param sort_by: The field to sort by: "first_place", "second_place", "third_place", "cup_finals", "cup_wins".
    :param limit: The number of top teams to show.
    :return: A list of ranked teams with all fields displayed.
    """
    if not league:
        print("League table must be specified!")
        return []

    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()

    # Query for league-based stats (retrieving all relevant fields)
    query = f"""
    SELECT name, first_place, second_place, third_place, cup_finals, cup_wins
    FROM {league}
    ORDER BY first_place DESC, second_place DESC, third_place DESC, cup_wins DESC, cup_finals DESC, name ASC
    LIMIT ?
    """
    c.execute(query, (limit,))
    results = c.fetchall()

    conn.close()

    # Print the ranked teams along with all fields
    print(f"--- Best Teams in {league.replace('_', ' ').title()} Ranked by First Place Finishes ---")
    for rank, row in enumerate(results, start=1):
        team_name, first_place, second_place, third_place, cup_finals, cup_wins = row
        print(f"{rank}. {team_name}:")
        print(f"   First Place Finishes: {first_place}")
        print(f"   Second Place Finishes: {second_place}")
        print(f"   Third Place Finishes: {third_place}")
        print(f"   Cup Wins: {cup_wins}")
        print(f"   Cup Final Appearances: {cup_finals} \n")

    return results


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
    """
     Display detailed statistics of a given team including league and European competition stats.

     :param team: Team object representing the selected team.
     :param league: Name of the league table in the database.
     """
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
        (gen_name, country, skill, league_titles, cup_titles, ucl, uel, uecl, europe) = general
        # Access the column values from League table
        (
            league_name, matches_played, wins, draws, losses, points, goals_scored, goals_against,
            first_place, second_place, third_place, cup_finals, cup_wins
        ) = league

        # Print the values
        print("\n--- Team Statistics ---")
        print(f"Name: {gen_name}")
        print(f"Country: {country}")
        print(f"Skill: {skill}")
        print(f"Matches Played: {matches_played}")
        print(f"Wins: {wins}")
        print(f"Draws: {draws}")
        print(f"Losses: {losses}")
        print(f"Points: {points}")
        print(f"Goals Scored: {goals_scored}")
        print(f"Goals Against: {goals_against}")

        print(f"League Titles: {league_titles}")
        print(f"Second Place Finishes: {second_place}")
        print(f"Third Place Finishes: {third_place}")

        print(f"Cup Wins: {cup_titles}")
        print(f"Cup Final Appearances: {cup_finals}")

        print(f"UCL Wins: {ucl}")
        print(f"UEL Wins: {uel}")
        print(f"UECL Wins: {uecl}")
        print(f"Latest European Qualification: {europe}")

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
           round_of_16 INTEGER DEFAULT 0,
           quarter_finals INTEGER DEFAULT 0,
           semi_finals INTEGER DEFAULT 0,
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
        c.execute(f"INSERT INTO {competition_table} VALUES (?, ?, ?, ?, ?, ?, ?)", (team_name, appearances, 0, 0, 0, 0, 0))
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
    c.execute(
        f"SELECT wins, finals, semi_finals, quarter_finals, round_of_16 FROM {competition_table} WHERE team_name=?",
        (team_name,))
    row = c.fetchone()

    wins, finals, semi_finals, quarter_finals, round_of_16 = row
    if round == "winner":
        wins += 1
        c.execute(f"UPDATE {competition_table} SET wins=? WHERE team_name=?",
                  (wins, team_name))
    elif round == "finals":
        finals += 1
        c.execute(f"UPDATE {competition_table} SET finals=? WHERE team_name=?",
                  (finals, team_name))
    elif round == "semi_finals":
        semi_finals += 1
        c.execute(f"UPDATE {competition_table} SET semi_finals=? WHERE team_name=?",
                  (semi_finals, team_name))
    elif round == "quarter_finals":
        quarter_finals += 1
        c.execute(f"UPDATE {competition_table} SET quarter_finals=? WHERE team_name=?",
                  (quarter_finals, team_name))
    elif round == "round_of_16":
        round_of_16 += 1
        c.execute(f"UPDATE {competition_table} SET round_of_16=? WHERE team_name=?",
                  (round_of_16, team_name))

    conn.commit()
    conn.close()

def get_european_competition_stats(competition):
    conn = sqlite3.connect(COMPETITIONS_DB)
    c = conn.cursor()

    # Replace spaces with underscores for table names
    competition_table = competition.replace(" ", "")

    query = f"""
        SELECT team_name, appearances, round_of_16, quarter_finals, semi_finals, finals, wins
        FROM {competition_table}
        ORDER BY wins DESC, finals DESC, semi_finals DESC, quarter_finals DESC, round_of_16 DESC, appearances DESC, team_name ASC
    """
    c.execute(query)
    stats = c.fetchall()
    conn.close()

    # Display the results with ranking
    print(f"--- {competition} Stats (Ordered by Wins) ---")
    for rank, team in enumerate(stats, start=1):
        team_name, appearances, round_of_16, quarter_finals, semi_finals, finals, wins = team
        print(f"{rank}. {team_name}:\n"
              f"   Total Appearances: {appearances}, "
              f"Round of 16: {round_of_16}, "
              f"Quarter-Finals: {quarter_finals}, "
              f"Semi-Finals: {semi_finals}, "
              f"Finals: {finals}, "
              f"Wins: {wins}\n")

    return stats
