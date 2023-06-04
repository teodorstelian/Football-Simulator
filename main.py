import database
import leagues
import matches
import teams as Teams

db, country_teams = leagues.select_league()

database.create_teams_table(db)  # Create the teams table if it doesn't exist

cur_teams = database.get_teams(db)  # Retrieve teams from the database

if len(cur_teams) == 0:
    cur_teams = Teams.generate_teams(country_teams, db)

matches.generate_fixtures(cur_teams)

for team in cur_teams:
    database.update_team(team, db)  # Update team data in the database

teams = database.get_teams(db)  # Retrieve teams with updated data from the database
matches.generate_standings(teams)
