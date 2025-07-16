class Contact:
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