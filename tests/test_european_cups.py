from src.settings import ALL_COUNTRIES


def calculate_teams_by_round(competition_name):
    """
    Helper function to calculate teams for each round for a given competition.
    Splits counts into first and second round.

    :param competition_name: The name of the European competition (UCL, UEL, UECL)
    :return: A tuple with total teams in (first_round, second_round)
    """
    first_round_teams = 0
    second_round_teams = 0

    for country in ALL_COUNTRIES:
        europe_places = country.get("europe", {})
        if competition_name in europe_places:
            # Add the number of teams for each round
            first_round_teams += europe_places[competition_name][0]
            second_round_teams += europe_places[competition_name][1]

    return first_round_teams, second_round_teams


def is_power_of_two(number):
    """
    Helper function to check if a number is a power of 2.
    :param number: Integer to check
    :return: True if the number is a power of 2, False otherwise
    """
    return number > 0 and (number & (number - 1)) == 0


def test_teams_by_round_UCL():
    """Test the distribution of teams for UCL by rounds."""
    first_round, second_round = calculate_teams_by_round("UCL")
    print(f"UCL - First Round: {first_round}, Second Round: {second_round}")
    assert second_round == 2 * first_round
    assert is_power_of_two(first_round), f"First round teams in UCL ({first_round}) are not a power of 2!"
    assert is_power_of_two(second_round), f"Second round teams in UCL ({second_round}) are not a power of 2!"


def test_teams_by_round_UEL():
    """Test the distribution of teams for UEL by rounds."""
    first_round, second_round = calculate_teams_by_round("UEL")
    print(f"UEL - First Round: {first_round}, Second Round: {second_round}")
    assert second_round == 2 * first_round
    assert is_power_of_two(first_round), f"First round teams in UEL ({first_round}) are not a power of 2!"
    assert is_power_of_two(second_round), f"Second round teams in UEL ({second_round}) are not a power of 2!"


def test_teams_by_round_UECL():
    """Test the distribution of teams for UECL by rounds."""
    first_round, second_round = calculate_teams_by_round("UECL")
    print(f"UECL - First Round: {first_round}, Second Round: {second_round}")
    assert second_round == 2 * first_round
    assert is_power_of_two(first_round), f"First round teams in UECL ({first_round}) are not a power of 2!"
    assert is_power_of_two(second_round), f"Second round teams in UECL ({second_round}) are not a power of 2!"
