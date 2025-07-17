from datetime import datetime, date


class ContactBook:
    def __init__(self):
        self.contacts = {}

    def _get_actual_key(self, name):
        for stored_name in self.contacts:
            if stored_name.lower() == name.lower():
                return stored_name
        return None

    def add_contact(self, contact):
        if self._get_actual_key(contact.name):
            return False
        self.contacts[contact.name] = contact
        return True


    def find(self, name):
        actual_key = self._get_actual_key(name)
        return self.contacts.get(actual_key)

    def edit_contact(self, current_name, **kwargs):
        actual_key = self._get_actual_key(current_name)
        contact = self.contacts.get(actual_key)
        if not contact:
            return False

        new_name = kwargs.get("name")
        if new_name and new_name.lower() != actual_key.lower():
            if self._get_actual_key(new_name):
                print(f"Cannot rename to '{new_name}': already exists.")
                return False

            self.contacts.pop(actual_key)
            self.contacts[new_name] = contact

        for key, value in kwargs.items():
            setattr(contact, key, value)

        return True


    def delete_contact(self, name):
        actual_key = self._get_actual_key(name)
        if actual_key:
            return self.contacts.pop(actual_key)
        return None

    def search_contacts(self, query: str):
    query = query.lower()
    results = []
    for contact in self.contacts.values():
        fields = [
            contact.name,
            contact.phone,
            contact.email,
            contact.address,
            contact.birthday
        ]
        if any(f and query in f.lower() for f in fields):
            results.append(contact)
    return results

    def days_to_birthday(self, birthday_str):
        try:
            birthday = datetime.strptime(birthday_str, "%Y-%m-%d").date()
        except ValueError:
            return "Invalid birthday format. Expected YYYY-MM-DD."

        today = date.today()
        this_year_birthday = date(today.year, birthday.month, birthday.day)

        if this_year_birthday < today:
            next_birthday = date(today.year + 1, birthday.month, birthday.day)
        else:
            next_birthday = this_year_birthday

        return (next_birthday - today).days
