from datetime import datetime, date
from typing import Optional, List, Union

from models.contact import Contact


class ContactBook:
    """
    Manages a collection of contacts, providing methods to add, edit, delete, and search contacts,
    as well as calculate days until a contact's next birthday.
    """

    def __init__(self):
        self.contacts = {}

    def _get_actual_key(self, name: str) -> Optional[str]:
        """
        Returns the actual key in the contacts dictionary that matches the given name case-insensitively.

        Args:
            name (str): The name to search for.

        Returns:
            Optional[str]: The matched key from the dictionary, or None if not found.
        """

        for stored_name in self.contacts:
            if stored_name.lower() == name.lower():
                return stored_name
        return None

    def add_contact(self, contact: Contact) -> bool:
        """
        Adds a contact to the book if the name does not already exist (case-insensitive).

        Args:
            contact (Contact): The contact object to add.

        Returns:
            bool: True if added successfully, False if a contact with the same name already exists.
        """

        if self._get_actual_key(contact.name):
            return False
        self.contacts[contact.name] = contact
        return True


    def find(self, name: str) -> Optional[Contact]:
        """
        Finds and returns a contact by name.

        Args:
            name (str): The name of the contact to find.

        Returns:
            Optional[Contact]: The found Contact object, or None if not found.
        """

        actual_key = self._get_actual_key(name)
        return self.contacts.get(actual_key)

    def edit_contact(self, current_name: str, **kwargs) -> bool:
        """
        Edits a contact's attributes, including renaming it.

        Args:
            current_name (str): The current name of the contact to edit.
            **kwargs: Fields to update (e.g., name, phone, email, address, birthday).

        Returns:
            bool: True if the contact was successfully edited, False otherwise.
        """

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


    def delete_contact(self, name: str) -> Optional[Contact]:
        """
        Deletes a contact by name.

        Args:
            name (str): The name of the contact to delete.

        Returns:
            Optional[Contact]: The deleted Contact object, or None if not found.
        """

        actual_key = self._get_actual_key(name)
        if actual_key:
            return self.contacts.pop(actual_key)
        return None

    def search_contacts(self, query: str) -> List[Contact]:
        """
        Searches contacts by partial name match (case-insensitive).

        Args:
            query (str): The substring to search in contact names.

        Returns:
            List[Contact]: A list of matching Contact objects.
        """

        return [c for c in self.contacts.values() if query.lower() in c.name.lower()]

    def days_to_birthday(self, birthday_str: str) -> Union[int, str]:
        """
        Calculates the number of days until the next birthday based on a given date string.

        Args:
            birthday_str (str): Birthday in 'YYYY-MM-DD' format.

        Returns:
            Union[int, str]: Days remaining until next birthday, or error string if the date is invalid.
        """

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
