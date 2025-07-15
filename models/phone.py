from models.field import Field


class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val: str):
        if not val.isdigit() or len(val) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        self._value = val
