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


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Error: {str(e)}"
    return wrapper
