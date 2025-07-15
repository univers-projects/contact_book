from datetime import timedelta, datetime



class ContactBook:
    def __init__(self):
        self.contacts = {}  # Stores contacts with original casing

    def _get_actual_key(self, name):
        # Find actual key (original casing) by lowercased match
        for stored_name in self.contacts:
            if stored_name.lower() == name.lower():
                return stored_name
        return None

    def add_contact(self, contact):
        self.contacts[contact.name] = contact

    def find(self, name):
        actual_key = self._get_actual_key(name)
        return self.contacts.get(actual_key)

    def edit_contact(self, name, **kwargs):
        contact = self.find(name)
        if not contact:
            return False
        for key, value in kwargs.items():
            setattr(contact, key, value)
        return True

    def delete_contact(self, name):
        actual_key = self._get_actual_key(name)
        if actual_key:
            return self.contacts.pop(actual_key)
        return None

    def search_contacts(self, query):
        return [c for c in self.contacts.values() if query.lower() in c.name.lower()]

