from models.note import Note

class NoteBook:
    def __init__(self):
        self.notes = []

    def add_note(self, text, tags=None):
        self.notes.append(Note(text, tags))

    def search_notes(self, keyword):
        return [note for note in self.notes if keyword.lower() in note.text.lower() or keyword in note.tags]

    def delete_note(self, text):
        self.notes = [n for n in self.notes if n.text != text]

