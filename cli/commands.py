from services.contact_book import ContactBook
from utils.utils import input_error


@input_error
def add_birthday(args, book: ContactBook):
    name, bday = args
    record = book.find(name)
    if not record:
        raise ValueError("Contact not found.")
    record.add_birthday(bday)
    return "Birthday added."


@input_error
def birthdays(args, book: ContactBook):
    result = book.get_upcoming_birthdays()
    if not result:
        return "No birthdays in the next 7 days."
    return "\n".join(
        f"{item['name']} will be congratulated on {item['congratulation_date']}"
        for item in result
    )


@input_error
def show_birthday(args, book: ContactBook):
    name = args[0]
    record = book.find(name)
    if not record:
        raise ValueError("Contact not found.")
    if not record.birthday:
        return "Birthday not set."
    return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}"


@input_error
def add_contact(args, book: ContactBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_phone(args, book: ContactBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        raise ValueError("Contact not found.")
    if record.edit_phone(old_phone, new_phone):
        return "Phone number updated."
    return "Phone number not found."


@input_error
def show_phone(args, book: ContactBook):
    name = args[0]
    record = book.find(name)
    if not record:
        raise ValueError("Contact not found.")
    return "; ".join(phone.value for phone in record.phones)


def show_all(book: ContactBook):
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())

