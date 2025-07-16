from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from cli.commands import (
    add_contact, search_contact, add_note, search_note, list_notes, list_contacts,
    edit_contact, delete_contact, edit_note, delete_note, show_birthday, show_commands, birthdays
)
from services.contact_book import ContactBook
from services.note_book import NoteBook
from utils.utils import load_data, save_data

commands = {
    "add contact": add_contact,
    "search contact": search_contact,
    "edit contact": edit_contact,
    "delete contact": delete_contact,
    "show contacts": list_contacts,
    "add note": add_note,
    "search note": search_note,
    "edit note": edit_note,
    "delete note": delete_note,
    "show notes": list_notes,
    "show birthday": show_birthday,
    "commands": show_commands,
    "birthdays": (birthdays, "contact"),
}


command_completer = WordCompleter(commands.keys(), ignore_case=True)

style = Style.from_dict({
    '': '#00aaaa',
    'prompt': 'bold',
})

def run_command_loop():
    contact_book = ContactBook()
    note_book = NoteBook()

    contact_book.contacts = load_data("addressbook.pkl") or {}
    note_book.notes = load_data("notes.pkl") or []

    print("Welcome to the assistant bot!")

    session = PromptSession(auto_suggest=AutoSuggestFromHistory(), completer=command_completer, style=style)

    while True:
        try:
            user_input = session.prompt(">>> ", complete_while_typing=True).strip().lower()

            if user_input in ("exit", "close"):
                save_data(contact_book.contacts, "addressbook.pkl")
                save_data(note_book.notes, "notes.pkl")
                print("Good bye!")
                break

            matched = next((cmd for cmd in commands if user_input.startswith(cmd)), None)

            if matched:
                entry = commands[matched]
                if isinstance(entry, tuple):
                    func, target = entry
                    context = contact_book if target == "contact" else note_book
                else:
                    func = entry
                    context = contact_book if "contact" in matched else note_book

                print(func(None, context))
            else:
                print("Unknown command. Type 'commands' to see available options.")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break
