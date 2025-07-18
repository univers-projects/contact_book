import pickle
from typing import Any, Callable, Optional


def save_data(book: Any, file_path: str) -> None:
    """
    Save a Python object to a file using pickle.

    Args:
        book (Any): The object to serialize and save.
        file_path (str): The path to the file where the object will be stored.
    """
    with open(file_path, "wb") as f:
        pickle.dump(book, f)


def load_data(file_path: str) -> Optional[Any]:
    """
    Load a Python object from a pickle file.

    Args:
        file_path (str): The path to the file to load from.

    Returns:
        Optional[Any]: The loaded object, or None if the file does not exist.
    """
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


def input_error(func: Callable) -> Callable:
    """
    Decorator that wraps a function and handles common input-related exceptions.

    Args:
        func (Callable): The function to wrap.

    Returns:
        Callable: A wrapped function that catches KeyError, ValueError, and IndexError,
                  and returns an error message string instead of raising an exception.
    """
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Error: {str(e)}"
    return wrapper
