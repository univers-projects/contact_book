import pickle
from datetime import datetime, timedelta


def save_data(book, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(book, f)


def load_data(file_path):
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


def days_until_birthday(birthday_str):
    today = datetime.today().date()
    bday = datetime.strptime(birthday_str, "%Y-%m-%d").date()
    bday_this_year = bday.replace(year=today.year)
    if bday_this_year < today:
        bday_this_year = bday_this_year.replace(year=today.year + 1)
    return (bday_this_year - today).days


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Error: {str(e)}"
    return wrapper
