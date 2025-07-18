class Contact:
    """
        Represents a contact with personal information such as name, phone, email, address, and birthday.

        Attributes:
            name (str): The name of the contact (required).
            phone (str): Phone number of the contact.
            email (str): Email address of the contact.
            address (str): Physical address of the contact.
            birthday (str): Birthday of the contact in 'YYYY-MM-DD' format.
    """

    def __init__(self, name, phone=None, email=None, address=None, birthday=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.birthday = birthday

    def __str__(self):
        return (
            f"Name: {self.name}, Phone: {self.phone}, "
            f"Email: {self.email}, Address: {self.address}, "
            f"Birthday: {self.birthday}"
        )