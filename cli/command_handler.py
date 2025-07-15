from models.contact import Contact
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
            save_data(note_book.notes, "notes.searapkl")
            print("Good bye!")
            break

        elif command.startswith("add contact"):
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            address = input("Address: ")
            birthday = input("Birthday (DD.MM.YYYY): ")
            try:
                contact_book.add_contact(Contact(name, phone, email, address, birthday))
                print("Contact added.")
            except ValueError as e:
                print("Error:", e)
        elif command.startswith("search contact"):
            q = input("Search: ")
            results = contact_book.search_contacts(q)
            for c in results:
                print(c)
        elif command.startswith("add note"):
            text = input("Note text: ")
            tags = input("Tags (comma-separated): ").split(',')
            note_book.add_note(text, tags)
            print("Note added.")
        elif command.startswith("search note"):
            keyword = input("Keyword or tag: ")
            results = note_book.search_notes(keyword)
            for n in results:
                print(f"{n.text} | Tags: {', '.join(n.tags)}")

        elif command.startswith("notes"):
            # Get all notes
            pass
        elif command.startswith("contacts"):
            # Get all contacts
            pass
        
        elif command.startswith("show birthday"):
            name = input("Name: ")
            contact = contact_book.find(name)
            if contact and contact.birthday:
                days = contact.birthday.days_to_birthday()
                bday_str = str(contact.birthday)
                print(f"{name}'s birthday is {bday_str}, it is in {days} days.")
            else:
                print("Birthday not found.")

        else:
            print("Unknown command. Try again.")
