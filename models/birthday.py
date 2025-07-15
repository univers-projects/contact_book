from datetime import datetime, date
from utils.date_helper import parse_birthday
from models.field import Field

class Birthday(Field):
    def __init__(self, val: str):
        self._value = parse_birthday(val)

    @property
    def value(self) -> date:
        return self._value

    @value.setter
    def value(self, val: str):
        self._value = parse_birthday(val)

    def days_to_birthday(self) -> int:
        """
        Returns number of days until the next birthday.
        """
        today = datetime.today().date()
        next_birthday = self._value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    def __str__(self):
        return self._value.strftime("%d.%m.%Y")