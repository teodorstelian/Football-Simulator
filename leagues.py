import settings


def select_league():
    print("1. Premier League (England) \n"
          "2. La Liga (Spain) \n"
          "3. Bundesliga (Germany) \n"
          "4. Ligue 1 (France) \n"
          "5. Serie A (Italy)")

    league_mapping = {
        '1': (settings.ENG_DB, settings.ENG_TEAMS),
        '2': (settings.ESP_DB, settings.ESP_TEAMS),
        '3': (settings.GER_DB, settings.GER_TEAMS),
        '4': (settings.FRA_DB, settings.FRA_TEAMS),
        '5': (settings.ITA_DB, settings.ITA_TEAMS),
    }

    league = input("Enter the league number: ")
    db, teams = league_mapping.get(league, (None, None))

    if db is None or teams is None:
        raise ValueError("Invalid value")

    print(f"Selected league: {league}")
    print(f"Database: {db}")
    print(f"Teams: {teams}")

    return db, teams
