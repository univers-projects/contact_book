from datetime import datetime

from models.field import Field


class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val: str):
        try:
            self._value = datetime.strptime(val, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")