from cli.commands import add_contact, search_contact, add_note, search_note, list_notes, list_contacts, edit_contact, \
    delete_contact, edit_note, delete_note, show_birthday
from services.contact_book import ContactBook
from services.note_book import NoteBook
from utils.utils import load_data, save_data


def run_command_loop():
    contact_book = ContactBook()
    contact_book_data = load_data(file_path="addressbook.pkl")
    if contact_book_data:
        contact_book.contacts = contact_book_data
    note_book = NoteBook()
    note_data = load_data(file_path="notes.pkl")
    if note_data:
        note_book.notes = note_data
    print("Welcome to the assistant bot! Enter a command:")

    while True:
        command = input(">>> ").strip().lower()
        print(command)

        if command in ["close", "exit"]:
            save_data(contact_book.contacts, "addressbook.pkl")
            save_data(note_book.notes, "notes.pkl")
            print("Good bye!")
            break


        if command.startswith("add contact"):
            args = command[len("add contact"):].strip().split()
            print(add_contact(args, contact_book))

        elif command.startswith("search contact"):
            args = command[len("search contact"):].strip().split()
            print(search_contact(args, contact_book))

        elif command.startswith("contacts"):
            args = command[len("contacts"):].strip().split()
            print(list_contacts(args, contact_book))

        elif command.startswith("edit contact"):
            args = command[len("edit contact"):].strip().split()
            print(args)
            print(edit_contact(args, contact_book))

        elif command.startswith("delete contact"):
            args = command[len("delete contact"):].strip().split()
            print(delete_contact(args, contact_book))

        elif command.startswith("show birthday"):
            args = command[len("show birthday"):].strip().split()
            print(show_birthday(args, contact_book))

        elif command.startswith("add note"):
            args = command[len("add note"):].strip().split()
            print(add_note(args, note_book))

        elif command.startswith("search note"):
            args = command[len("search note"):].strip().split()
            print(search_note(args, note_book))

        elif command.startswith("notes"):
            args = command[len("notes"):].strip().split()
            print(list_notes(args, note_book))

        elif command.startswith("edit note"):
            args = command[len("edit note"):].strip().split()
            print(edit_note(args, note_book))

        elif command.startswith("delete note"):
            args = command[len("delete note"):].strip().split()
            print(delete_note(args, note_book))
        else:
            print("Unknown command. Try again.")
