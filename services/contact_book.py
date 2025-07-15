from datetime import timedelta, datetime
import re

def is_valid_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def is_valid_phone(phone):
    return bool(re.match(r"^\+?\d{10,15}$", phone))


class ContactBook:
    def __init__(self):
        self.contacts = {}

    def add_contact(self, contact):
        if not is_valid_email(contact.email) or not is_valid_phone(contact.phone):
            raise ValueError("Invalid phone or email")
        self.contacts[contact.name] = contact

    def find(self, name):
        return self.contacts.get(name)

    def get_birthdays_in(self, days):
        return []

    def search_contacts(self, query):
        return [c for c in self.contacts.values() if query.lower() in c.name.lower()]

    def edit_contact(self, name, **kwargs):
        contact = self.contacts.get(name)
        if not contact:
            return False
        for key, value in kwargs.items():
            setattr(contact, key, value)
        return True

    def delete_contact(self, name):
        return self.contacts.pop(name, None)

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                bday_this_year = record.birthday.value.replace(year=today.year)
                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)
                delta_days = (bday_this_year - today).days
                if 0 <= delta_days < 7:
                    congrat_date = bday_this_year
                    if congrat_date.weekday() >= 5:
                        congrat_date += timedelta(days=(7 - congrat_date.weekday()))
                    upcoming.append({"name": record.name.value, "congratulation_date": congrat_date.strftime('%Y-%m-%d')})
        return upcoming
