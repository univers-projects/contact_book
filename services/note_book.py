from models.note import Note
from typing import List, Optional


class NoteBook:
    """
    Manages a list of notes with support for adding, editing, searching, and deleting notes.
    """

    def __init__(self):
        self.notes = []

    def add_note(self, text: str, tags: Optional[List[str]] = None) -> None:
        """
        Add a new note with text and optional tags.

        Args:
            text (str): The content of the note.
            tags (Optional[List[str]]): A list of tags to associate with the note.
        """

        self.notes.append(Note(text, tags))

    def edit_note(
        self, identifier: str, new_text: Optional[str] = None, new_tags: Optional[List[str]] = None) -> bool:
        """
        Edit a note identified by matching text or tag. Updates the text and/or tags if provided.

        Args:
            identifier (str): A keyword to find the note by text or tag.
            new_text (Optional[str]): The new text to replace the current note text.
            new_tags (Optional[List[str]]): New list of tags to replace current tags.

        Returns:
            bool: True if at least one note was edited, False otherwise.
        """

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

    def search_notes(self, keyword: str) -> List[Note]:
        """
        Search notes by keyword in text or tag (case-insensitive).

        Args:
            keyword (str): The keyword to search for.

        Returns:
            List[Note]: A list of notes matching the keyword.
        """

        return [note for note in self.notes if keyword.lower() in note.text.lower() or keyword in note.tags]

    def delete_note(self, text: str) -> None:
        """
        Delete a note by exact text match.

        Args:
            text (str): The exact text of the note to delete.
        """

        self.notes = [n for n in self.notes if n.text != text]
