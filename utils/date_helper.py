from datetime import datetime, date

def parse_birthday(date_str: str) -> date:
    """
    Validates and parses a birthday string in DD.MM.YYYY format.

    Args:
        date_str (str): A date string like "15.07.1990"

    Returns:
        date: A datetime.date object

    Raises:
        ValueError: if the format is incorrect
    """
    try:
        return datetime.strptime(date_str, "%d.%m.%Y").date()
    except ValueError:
        raise ValueError("Invalid date format. Use DD.MM.YYYY")