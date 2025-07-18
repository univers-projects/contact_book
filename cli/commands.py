import re
from datetime import date, datetime
from tabulate import tabulate
from colorama import Fore, Style, init

from models.contact import Contact
from services.contact_book import ContactBook
from utils.utils import input_error
from services.note_book import NoteBook

init(autoreset=True)


def is_valid_email(email: str) -> bool:
    """
    Check if the given email address is valid.

    Args:
        email (str): Email address to validate.

    Returns:
        bool: True if valid, False otherwise.
    """

    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def is_valid_phone(phone: str) -> bool:
    """
    Validate the phone number format.

    Args:
        phone (str): Phone number to validate.

    Returns:
        bool: True if valid, False otherwise.
    """

    return bool(re.match(r"^\+?\d{10,15}$", phone))


def is_valid_birthday(birthday_str: str) -> bool:
    """
    Validate the birthday format and ensure it is not in the future.

    Args:
        birthday_str (str): Birthday string in 'YYYY-MM-DD' format.

    Returns:
        bool: True if valid and not in future, False otherwise.
    """

    try:
        bday = datetime.strptime(birthday_str, "%Y-%m-%d").date()
        return bday <= date.today()
    except ValueError:
        return False


@input_error
def add_contact(contact_book: ContactBook) -> str:
    """
    Prompt user for contact details and add a new contact to the book.

    Args:
        contact_book (ContactBook): Instance of the contact book.

    Returns:
        str: Success or error message.
    """

    while True:
        name = input(f"{Fore.CYAN}Name:{Style.RESET_ALL} ").strip().title()
        if not name:
            print(f"{Fore.RED}Name is required.{Style.RESET_ALL}")
            continue
        if contact_book.find(name):
            print(f"{Fore.YELLOW}Contact with name '{name}' already exists. Please choose a different name.{Style.RESET_ALL}")
            continue
        break

    while True:
        phone = input(f"{Fore.CYAN}Phone:{Style.RESET_ALL} ").strip()
        if is_valid_phone(phone):
            break
        print(f"{Fore.RED}Invalid phone number. Please enter a valid phone (10–15 digits, optional '+' at start).{Style.RESET_ALL}")

    while True:
        email = input(f"{Fore.CYAN}Email (optional):{Style.RESET_ALL} ").strip()
        if not email:
            break
        if is_valid_email(email):
            break
        print(f"{Fore.RED}Invalid email address. Please enter a valid email or press Enter to skip.{Style.RESET_ALL}")

    address = input(f"{Fore.CYAN}Address (optional):{Style.RESET_ALL} ").strip()
    while True:
        birthday = input(f"{Fore.CYAN}Birthday (YYYY-MM-DD):{Style.RESET_ALL} ").strip()
        if not birthday:
            break
        if is_valid_birthday(birthday):
            break
        print(f"{Fore.RED}Invalid birthday. Please use YYYY-MM-DD and ensure the date is not in the future.{Style.RESET_ALL}")

    contact = Contact(name, phone, email, address, birthday)
    success = contact_book.add_contact(contact)

    if not success:
        return f"{Fore.YELLOW}Contact with name '{name}' already exists.{Style.RESET_ALL}"
    return f"{Fore.GREEN}Contact added.{Style.RESET_ALL}"



@input_error
def search_contact(contact_book: ContactBook) -> str:
    """
    Search for contacts by name and return matching results.

    Args:
        contact_book (ContactBook): Instance of the contact book.

    Returns:
        str: Tabulated results or error message.
    """

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
def edit_contact(contact_book: ContactBook) -> str:
    """
    Edit an existing contact's field by name.

    Args:
        contact_book (ContactBook): Instance of the contact book.

    Returns:
        str: Update status message.
    """

    name = input(f"{Fore.CYAN}Contact name to edit:{Style.RESET_ALL} ").strip()
    contact = contact_book.find(name)
    if not contact:
        return f"{Fore.RED}Contact '{name}' not found. Add a new contact instead.{Style.RESET_ALL}"

    field = input(f"{Fore.CYAN}Field to edit (name, phone, email, address, birthday):{Style.RESET_ALL} ").strip().lower()
    if field not in ["name", "phone", "email", "address", "birthday"]:
        return f"{Fore.RED}Invalid field. Please choose one of: name, phone, email, address, birthday.{Style.RESET_ALL}"

    if field == "name":
        while True:
            new_name = input(f"{Fore.CYAN}New name:{Style.RESET_ALL} ").strip().title()
            if not new_name:
                print(f"{Fore.RED}Name cannot be empty.{Style.RESET_ALL}")
                continue
            if contact_book.find(new_name):
                print(f"{Fore.YELLOW}A contact with the name '{new_name}' already exists. Choose a different name.{Style.RESET_ALL}")
                continue
            break

        contact_book.delete_contact(name)
        contact.name = new_name
        contact_book.add_contact(contact)
        return f"{Fore.GREEN}Contact renamed to '{new_name}'.{Style.RESET_ALL}"

    elif field == "phone":
        while True:
            new_value = input(f"{Fore.CYAN}New phone number:{Style.RESET_ALL} ").strip()
            if is_valid_phone(new_value):
                break
            print(f"{Fore.RED}Invalid phone number. Please enter a valid phone (10–15 digits, optional '+' at start).{Style.RESET_ALL}")

    elif field == "email":
        while True:
            new_value = input(f"{Fore.CYAN}New email address:{Style.RESET_ALL} ").strip()
            if is_valid_email(new_value):
                break
            print(f"{Fore.RED}Invalid email address. Please enter a valid format (e.g. name@example.com).{Style.RESET_ALL}")

    elif field == "birthday":
        while True:
            new_value = input(f"{Fore.CYAN}New birthday (YYYY-MM-DD):{Style.RESET_ALL} ").strip()
            if is_valid_birthday(new_value):
                break
            print(f"{Fore.RED}Invalid birthday. Please use YYYY-MM-DD and ensure the date is not in the past.{Style.RESET_ALL}")

    elif field == "address":
        new_value = input(f"{Fore.CYAN}New address:{Style.RESET_ALL} ").strip()

    success = contact_book.edit_contact(name, **{field: new_value})
    if success:
        updated_contact = contact_book.find(name)
        return f"{Fore.GREEN}Contact '{updated_contact.name}' updated.{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}Contact '{name}' not found.{Style.RESET_ALL}"
    

@input_error
def delete_contact(contact_book: ContactBook) -> str:
    """
    Delete a contact by name.

    Args:
        contact_book (ContactBook): Instance of the contact book.

    Returns:
        str: Success or failure message.
    """

    name = input(f"{Fore.CYAN}Name of the contact to delete:{Style.RESET_ALL} ").strip()
    removed = contact_book.delete_contact(name)
    return (
        f"{Fore.GREEN}Deleted contact: {name}{Style.RESET_ALL}"
        if removed else
        f"{Fore.RED}Contact '{name}' not found.{Style.RESET_ALL}"
    )


@input_error
def list_contacts(contact_book: ContactBook) -> str:
    """
    List all contacts in the contact book.

    Args:
        contact_book (ContactBook): Instance of the contact book.

    Returns:
        str: Tabulated list of contacts.
    """

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
def add_note(note_book: NoteBook) -> str:
    """
    Prompt user to add a new note with optional tags.

    Args:
        note_book (NoteBook): Instance of the note book.

    Returns:
        str: Success message.
    """

    text = input(f"{Fore.CYAN}Note text:{Style.RESET_ALL} ").strip()
    tags_input = input(f"{Fore.CYAN}Tags (comma-separated, optional):{Style.RESET_ALL} ").strip()
    tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
    note_book.add_note(text, tags)
    return f"{Fore.GREEN}Note added.{Style.RESET_ALL}"


@input_error
def search_note(note_book: NoteBook) -> str:
    """
    Search for notes by keyword or tag.

    Args:
        note_book (NoteBook): Instance of the note book.

    Returns:
        str: Search result or error message.
    """

    keyword = input(f"{Fore.CYAN}Keyword or tag to search:{Style.RESET_ALL} ").strip()
    results = note_book.search_notes(keyword)
    return (
        "\n".join(f"{Fore.YELLOW}Note:{Style.RESET_ALL} {n.text} | {Fore.MAGENTA}Tags:{Style.RESET_ALL} {', '.join(n.tags)}" for n in results)
        or f"{Fore.RED}No notes found.{Style.RESET_ALL}"
    )


@input_error
def list_notes(note_book: NoteBook) -> str:
    """
    List all notes with their tags.

    Args:
        note_book (NoteBook): Instance of the note book.

    Returns:
        str: Tabulated list of notes.
    """

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
def edit_note(note_book: NoteBook) -> str:
    """
    Edit the text and/or tags of a note identified by text or tag.

    Args:
        note_book (NoteBook): Instance of the note book.

    Returns:
        str: Update status message.
    """

    identifier = input(f"{Fore.CYAN}Enter note text or tag to edit:{Style.RESET_ALL} ").strip()
    new_text = input(f"{Fore.CYAN}New text:{Style.RESET_ALL} ").strip()

    new_tags = None
    update_tags = input(f"{Fore.CYAN}Do you want to edit tags as well? (yes/no):{Style.RESET_ALL} ").strip().lower()

    if update_tags == "yes":
        tags_input = input(f"{Fore.CYAN}Enter new tags (comma-separated):{Style.RESET_ALL} ").strip()
        new_tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
    elif update_tags not in ["no", ""]:
        print(f"{Fore.YELLOW}Unknown response. Tags will not be updated.{Style.RESET_ALL}")

    edited = note_book.edit_note(identifier, new_text=new_text, new_tags=new_tags)

    return (
        f"{Fore.GREEN}Note(s) updated.{Style.RESET_ALL}" if edited else f"{Fore.RED}Note not found.{Style.RESET_ALL}"
    )


@input_error
def delete_note(note_book: NoteBook) -> str:
    """
    Delete notes that match a given text or tag.

    Args:
        note_book (NoteBook): Instance of the note book.

    Returns:
        str: Deletion status message.
    """

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
def show_birthday(contact_book: ContactBook):
    """
    Show how many days are left until a contact’s birthday.

    Args:
        contact_book (ContactBook): Instance of the contact book.

    Returns:
        str: Birthday info or error.
    """

    name = input(f"{Fore.CYAN}Name:{Style.RESET_ALL} ").strip()
    contact = contact_book.find(name)

    if contact and contact.birthday:
        days = contact_book.days_to_birthday(contact.birthday)
        return f"{Fore.YELLOW}{name}'s birthday is on {contact.birthday}, in {days} days.{Style.RESET_ALL}"
    return f"{Fore.RED}Birthday not found.{Style.RESET_ALL}"


@input_error
def birthdays(contact_book: ContactBook) -> str:
    """
    Show upcoming birthdays within a given number of days.

    Args:
        contact_book (ContactBook): Instance of the contact book.

    Returns:
        str: Tabulated list of birthdays or message.
    """

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
def show_commands(*args) -> str:
    """
    Show a list of all available commands.

    Args:
        *args (Any): Ignored, for compatibility.

    Returns:
        str: Formatted list of commands.
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
