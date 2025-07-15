import re
from datetime import datetime

from models.contact import Contact
from services.contact_book import ContactBook
from utils.utils import input_error
from services.note_book import NoteBook


def is_valid_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def is_valid_phone(phone):
    return bool(re.match(r"^\+?\d{10,15}$", phone))


def is_valid_birthday(birthday_str: str) -> bool:
    try:
        datetime.strptime(birthday_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


@input_error
def add_contact(args, contact_book: ContactBook):
    name = input("Name: ").strip()
    if not name:
        raise ValueError("Name is required.")

    phone = input("Phone: ").strip()
    if not is_valid_phone(phone):
        raise ValueError("Invalid phone number")

    email = input("Email (optional): ").strip()
    if email and not is_valid_email(email):
        raise ValueError("Invalid email address")

    address = input("Address (optional): ").strip()
    birthday = input("Birthday (YYYY-MM-DD, optional): ").strip()
    if birthday and not is_valid_birthday(birthday):
        raise ValueError("Invalid birthday. Use YYYY-MM-DD")

    contact = Contact(name, phone, email, address, birthday)
    contact_book.add_contact(contact)
    return "Contact added."


@input_error
def search_contact(_, contact_book: ContactBook):
    query = input("Search query (name): ").strip()
    results = contact_book.search_contacts(query)
    return "\n".join(str(vars(c)) for c in results) or "No contacts found."


@input_error
def edit_contact(_, contact_book: ContactBook):
    name = input("Contact name to edit: ").strip()
    field = input("Field to edit (name, phone, email, address, birthday): ").strip()
    value = input(f"New value for {field}: ").strip()

    success = contact_book.edit_contact(name, **{field: value})
    if success:
        return f"Contact '{name}' updated."
    return f"Contact '{name}' not found."


@input_error
def delete_contact(_, contact_book: ContactBook):
    name = input("Name of the contact to delete: ").strip()
    removed = contact_book.delete_contact(name)
    return f"Deleted contact: {name}" if removed else f"Contact '{name}' not found."


@input_error
def list_contacts(_, contact_book: ContactBook):
    if contact_book.contacts:
        return "\n".join(f"{name}: {vars(c)}" for name, c in contact_book.contacts.items())
    return "No contacts found."


@input_error
def add_note(_, note_book: NoteBook):
    text = input("Note text: ").strip()
    tags_input = input("Tags (comma-separated, optional): ").strip()
    tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
    note_book.add_note(text, tags)
    return "Note added."


@input_error
def search_note(_, note_book: NoteBook):
    keyword = input("Keyword or tag to search: ").strip()
    results = note_book.search_notes(keyword)
    return "\n".join(f"{n.text} | Tags: {', '.join(n.tags)}" for n in results) or "No notes found."


@input_error
def list_notes(_, note_book: NoteBook):
    if note_book.notes:
        return "\n".join(f"{n.text} | Tags: {', '.join(n.tags)}" for n in note_book.notes)
    return "No notes found."


@input_error
def edit_note(_, note_book: NoteBook):
    identifier = input("Enter note text or tag to edit: ").strip()
    new_text = input("New text: ").strip()

    edited = False
    for note in note_book.notes:
        if note.text == identifier or identifier in note.tags:
            note.text = new_text
            edited = True

    return "Note(s) updated." if edited else "Note not found."


@input_error
def delete_note(_, note_book: NoteBook):
    identifier = input("Enter note text or tag to delete: ").strip()
    original_len = len(note_book.notes)

    note_book.notes = [
        note for note in note_book.notes
        if note.text != identifier and identifier not in note.tags
    ]

    return "Note(s) deleted." if len(note_book.notes) < original_len else "Note not found."


@input_error
def show_birthday(_, contact_book):
    name = input("Name: ").strip()
    contact = contact_book.find(name)

    if contact and contact.birthday:
        days = contact_book.days_to_birthday(contact.birthday)
        return f"{name}'s birthday is on {contact.birthday}, in {days} days."
    return "Birthday not found."
