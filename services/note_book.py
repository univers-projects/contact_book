from models.note import Note

class NoteBook:
    def __init__(self):
        self.notes = []

    def add_note(self, text, tags=None):
        self.notes.append(Note(text, tags))

    def edit_note(self, identifier, new_text=None, new_tags=None):
        edited = False
        identifier = identifier.lower()

        for note in self.notes:
            if identifier == note.text.lower() or identifier in [tag.lower() for tag in note.tags]:
                if new_text:
                    note.text = new_text
                if new_tags is not None:
                    note.tags = new_tags
                edited = True

        return edited

    def search_notes(self, keyword):
        return [note for note in self.notes if keyword.lower() in note.text.lower() or keyword in note.tags]

    def delete_note(self, text):
        self.notes = [n for n in self.notes if n.text != text]
