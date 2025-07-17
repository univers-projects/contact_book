import re
from datetime import datetime, date
from tabulate import tabulate
from colorama import Fore, Style, init

from models.contact import Contact
from services.contact_book import ContactBook
from utils.utils import input_error
from services.note_book import NoteBook

init(autoreset=True)

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
def add_contact(_, contact_book: ContactBook):
    name = input(f"{Fore.CYAN}Name:{Style.RESET_ALL} ").strip()
    if not name:
        raise ValueError("Name is required.")

    phone = input(f"{Fore.CYAN}Phone:{Style.RESET_ALL} ").strip()
    if not is_valid_phone(phone):
        raise ValueError("Invalid phone number")

    email = input(f"{Fore.CYAN}Email (optional):{Style.RESET_ALL} ").strip()
    if email and not is_valid_email(email):
        raise ValueError("Invalid email address")

    address = input(f"{Fore.CYAN}Address (optional):{Style.RESET_ALL} ").strip()
    birthday = input(f"{Fore.CYAN}Birthday (YYYY-MM-DD, optional):{Style.RESET_ALL} ").strip()
    if birthday and not is_valid_birthday(birthday):
        raise ValueError("Invalid birthday. Use YYYY-MM-DD")

    contact = Contact(name, phone, email, address, birthday)
    contact_book.add_contact(contact)
    return f"{Fore.GREEN}Contact added.{Style.RESET_ALL}"


@input_error
def search_contact(_, contact_book: ContactBook):
    query = input(f"{Fore.CYAN}Search query (name):{Style.RESET_ALL} ").strip()
    results = contact_book.search_contacts(query)

    if not results:
        return f"{Fore.RED}No contacts found.{Style.RESET_ALL}"

    table = []
    for contact in results:
        table.append([
            f"{Fore.YELLOW}{contact.name}{Style.RESET_ALL}",
            f"{Fore.CYAN}{contact.phone}{Style.RESET_ALL}",
            f"{Fore.MAGENTA}{contact.email or ''}{Style.RESET_ALL}",
            f"{Fore.BLUE}{contact.address or ''}{Style.RESET_ALL}",
            f"{Fore.GREEN}{contact.birthday or ''}{Style.RESET_ALL}",
        ])

    headers = [
        f"{Fore.YELLOW}Name{Style.RESET_ALL}",
        f"{Fore.CYAN}Phone{Style.RESET_ALL}",
        f"{Fore.MAGENTA}Email{Style.RESET_ALL}",
        f"{Fore.BLUE}Address{Style.RESET_ALL}",
        f"{Fore.GREEN}Birthday{Style.RESET_ALL}"
    ]

    return tabulate(table, headers=headers, tablefmt="grid")


@input_error
def edit_contact(_, contact_book: ContactBook):
    name = input(f"{Fore.CYAN}Contact name to edit:{Style.RESET_ALL} ").strip()
    field = input(f"{Fore.CYAN}Field to edit (name, phone, email, address, birthday):{Style.RESET_ALL} ").strip()
    value = input(f"{Fore.CYAN}New value for {field}:{Style.RESET_ALL} ").strip()

    if field == "name":
        contact = contact_book.find(name)
        if contact:
            contact_book.delete_contact(name)
            contact.name = value
            contact_book.add_contact(contact)
            return f"{Fore.GREEN}Contact renamed to '{value}'.{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}Contact '{name}' not found.{Style.RESET_ALL}"
    else:
        success = contact_book.edit_contact(name, **{field: value})
        return (
            f"{Fore.GREEN}Contact '{name}' updated.{Style.RESET_ALL}"
            if success else
            f"{Fore.RED}Contact '{name}' not found.{Style.RESET_ALL}"
        )


@input_error
def delete_contact(_, contact_book: ContactBook):
    name = input(f"{Fore.CYAN}Name of the contact to delete:{Style.RESET_ALL} ").strip()
    removed = contact_book.delete_contact(name)
    return (
        f"{Fore.GREEN}Deleted contact: {name}{Style.RESET_ALL}"
        if removed else
        f"{Fore.RED}Contact '{name}' not found.{Style.RESET_ALL}"
    )


@input_error
def list_contacts(_, contact_book: ContactBook):
    if not contact_book.contacts:
        return f"{Fore.RED}No contacts found.{Style.RESET_ALL}"

    table = []
    for contact in contact_book.contacts.values():
        table.append([
            f"{Fore.YELLOW}{contact.name}{Style.RESET_ALL}",
            f"{Fore.CYAN}{contact.phone}{Style.RESET_ALL}",
            f"{Fore.MAGENTA}{contact.email or ''}{Style.RESET_ALL}",
            f"{Fore.BLUE}{contact.address or ''}{Style.RESET_ALL}",
            f"{Fore.GREEN}{contact.birthday or ''}{Style.RESET_ALL}",
        ])

    headers = [
        f"{Fore.YELLOW}Name{Style.RESET_ALL}",
        f"{Fore.CYAN}Phone{Style.RESET_ALL}",
        f"{Fore.MAGENTA}Email{Style.RESET_ALL}",
        f"{Fore.BLUE}Address{Style.RESET_ALL}",
        f"{Fore.GREEN}Birthday{Style.RESET_ALL}"
    ]

    return tabulate(table, headers=headers, tablefmt="fancy_grid")


@input_error
def add_note(_, note_book: NoteBook):
    text = input(f"{Fore.CYAN}Note text:{Style.RESET_ALL} ").strip()
    tags_input = input(f"{Fore.CYAN}Tags (comma-separated, optional):{Style.RESET_ALL} ").strip()
    tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
    note_book.add_note(text, tags)
    return f"{Fore.GREEN}Note added.{Style.RESET_ALL}"


@input_error
def search_note(_, note_book: NoteBook):
    keyword = input(f"{Fore.CYAN}Keyword or tag to search:{Style.RESET_ALL} ").strip()
    results = note_book.search_notes(keyword)
    return (
        "\n".join(f"{Fore.YELLOW}Note:{Style.RESET_ALL} {n.text} | {Fore.MAGENTA}Tags:{Style.RESET_ALL} {', '.join(n.tags)}" for n in results)
        or f"{Fore.RED}No notes found.{Style.RESET_ALL}"
    )


@input_error
def list_notes(_, note_book: NoteBook):
    if not note_book.notes:
        return f"{Fore.RED}No notes found.{Style.RESET_ALL}"

    table = []
    for note in note_book.notes:
        table.append([
            f"{Fore.YELLOW}{note.text}{Style.RESET_ALL}",
            f"{Fore.MAGENTA}{', '.join(note.tags)}{Style.RESET_ALL}" if note.tags else ""
        ])

    headers = [f"{Fore.YELLOW}Note Text{Style.RESET_ALL}", f"{Fore.MAGENTA}Tags{Style.RESET_ALL}"]
    return tabulate(table, headers=headers, tablefmt="fancy_grid")


@input_error
def edit_note(_, note_book: NoteBook):
    identifier = input(f"{Fore.CYAN}Enter note text or tag to edit:{Style.RESET_ALL} ").strip()
    new_text = input(f"{Fore.CYAN}New text:{Style.RESET_ALL} ").strip()

    edited = False
    for note in note_book.notes:
        if note.text == identifier or identifier in note.tags:
            note.text = new_text
            edited = True

    return (
        f"{Fore.GREEN}Note(s) updated.{Style.RESET_ALL}" if edited else f"{Fore.RED}Note not found.{Style.RESET_ALL}"
    )


@input_error
def delete_note(_, note_book: NoteBook):
    identifier = input(f"{Fore.CYAN}Enter note text or tag to delete:{Style.RESET_ALL} ").strip()
    original_len = len(note_book.notes)

    note_book.notes = [
        note for note in note_book.notes
        if note.text != identifier and identifier not in note.tags
    ]

    return (
        f"{Fore.GREEN}Note(s) deleted.{Style.RESET_ALL}" if len(note_book.notes) < original_len
        else f"{Fore.RED}Note not found.{Style.RESET_ALL}"
    )


@input_error
def show_birthday(_, contact_book):
    name = input(f"{Fore.CYAN}Name:{Style.RESET_ALL} ").strip()
    contact = contact_book.find(name)

    if contact and contact.birthday:
        days = contact_book.days_to_birthday(contact.birthday)
        return f"{Fore.YELLOW}{name}'s birthday is on {contact.birthday}, in {days} days.{Style.RESET_ALL}"
    return f"{Fore.RED}Birthday not found.{Style.RESET_ALL}"


@input_error
def birthdays(_, contact_book):
    try:
        days = int(input("Show birthdays in how many days? ").strip())
    except ValueError:
        raise ValueError("Please enter a valid number of days.")

    matches = []

    for contact in contact_book.contacts.values():
        if contact.birthday:
            delta = contact_book.days_to_birthday(contact.birthday)
            if isinstance(delta, int) and delta <= days:
                matches.append([
                    f"{Fore.YELLOW}{contact.name}{Style.RESET_ALL}",
                    f"{Fore.GREEN}{contact.birthday}{Style.RESET_ALL}",
                    f"{Fore.CYAN}{delta} days{Style.RESET_ALL}"
                ])

    if not matches:
        return f"{Fore.RED}No upcoming birthdays in {days} days.{Style.RESET_ALL}"

    headers = [
        f"{Fore.YELLOW}Name{Style.RESET_ALL}",
        f"{Fore.GREEN}Birthday{Style.RESET_ALL}",
        f"{Fore.CYAN}In (Days){Style.RESET_ALL}"
    ]

    return tabulate(matches, headers=headers, tablefmt="fancy_grid")


@input_error
def show_commands(_, *args):
    """

    :param _:
    :param args:
    :return:
    """
    return f"""{Fore.GREEN}Available commands:{Style.RESET_ALL}
  {Fore.CYAN}📇 Contacts:{Style.RESET_ALL}
    {Fore.YELLOW}add contact{Style.RESET_ALL}                - Add a new contact
    {Fore.YELLOW}search contact{Style.RESET_ALL}             - Search contacts by name
    {Fore.YELLOW}edit contact{Style.RESET_ALL}               - Edit a contact field
    {Fore.YELLOW}delete contact{Style.RESET_ALL}             - Delete a contact
    {Fore.YELLOW}show contacts{Style.RESET_ALL}              - List all contacts
    {Fore.YELLOW}show birthday{Style.RESET_ALL}              - Show upcoming birthday for a contact
    {Fore.YELLOW}birthdays{Style.RESET_ALL}                  - Show upcoming birthday for a given number of days

  {Fore.CYAN}📝 Notes:{Style.RESET_ALL}
    {Fore.YELLOW}add note{Style.RESET_ALL}                   - Add a new note
    {Fore.YELLOW}search note{Style.RESET_ALL}                - Search notes by keyword or tag
    {Fore.YELLOW}edit note{Style.RESET_ALL}                  - Edit a note by text or tag
    {Fore.YELLOW}delete note{Style.RESET_ALL}                - Delete a note by text or tag
    {Fore.YELLOW}show notes{Style.RESET_ALL}                 - List all notes

  {Fore.CYAN}🚪 Exit:{Style.RESET_ALL}
    {Fore.YELLOW}exit / close{Style.RESET_ALL}               - Exit the assistant bot
    {Fore.YELLOW}commands{Style.RESET_ALL}                   - Show this command list
"""
