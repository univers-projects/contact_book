from models.birthday import Birthday

class Contact:
    def __init__(self, name, phone=None, email=None, address=None, birthday=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.birthday = Birthday(birthday) if birthday else None

    def __str__(self):
        bday = str(self.birthday) if self.birthday else "N/A"
        return (
            f"Name: {self.name}, Phone: {self.phone}, "
            f"Email: {self.email}, Address: {self.address}, "
            f"Birthday: {bday}"
        )