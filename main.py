import database
import matches
from teams import Team

database.create_teams_table()  # Create the teams table if it doesn't exist

teams = database.get_teams()  # Retrieve teams from the database

if len(teams) == 0:
    teams = [
        Team("Team A"),
        Team("Team B"),
        Team("Team C"),
        Team("Team D"),
    ]
    for team in teams:
        database.insert_team(team)  # Insert teams into the database

matches.generate_fixtures(teams)

for team in teams:
    database.update_team(team)  # Update team data in the database

teams = database.get_teams()  # Retrieve teams with updated data from the database
matches.generate_standings(teams)
