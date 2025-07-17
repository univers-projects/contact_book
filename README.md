# MemoMate Assistant Bot

MemoMate is a command-line assistant bot built in Python for managing contacts and notes. The bot provides a user-friendly interface to add, edit, delete, and search contacts and notes, along with additional features like birthday tracking, command suggestion, and colorful output formatting using Colorama.

---

## Features

### 📇 Contacts Management

* `add contact`: Add a new contact
* `search contact`: Search contacts by name
* `edit contact`: Edit a contact field (name, phone, email, address, birthday)
* `delete contact`: Delete a contact by name
* `show contacts`: List all contacts in a colored table
* `show birthday`: Show upcoming birthday for a contact with days left
* `birthdays`: Show upcoming birthday for a given number of days

### 📜 Notes Management

* `add note`: Add a note with optional tags
* `search note`: Search notes by keyword or tag
* `edit note`: Edit a note by text or tag
* `delete note`: Delete notes by text or tag
* `show notes`: List all notes in a colored table

### 🔹 System Commands

* `commands`: Display available commands
* `exit` / `close`: Exit the assistant bot

---

## Requirements

Install required packages:

```bash
pip install -r requirements.txt
```

### Key Dependencies:

* Python 3.10+
* `colorama`: For colored output in terminal

---

## How to Run

```bash
python main.py
```

You will see:

```
Welcome to the assistant bot! Enter a command:
>>>
```

Then type any supported command such as `add contact`, `add note`, etc.

---

## Smart Suggestions

The assistant uses `difflib.get_close_matches()` to suggest the nearest command when an unknown input is entered.

---

## Storage

* Contacts and notes are stored using `pickle` in `addressbook.pkl` and `notes.pkl` respectively.

---

## Notes

* Inputs are validated (e.g., phone, email, and birthday formats)
* Contact search/edit/delete is case-insensitive
* Notes can be filtered and edited by tag or content
* Friendly error handling via `@input_error` decorator

---

## License

This project is for demonstration and educational purposes.
