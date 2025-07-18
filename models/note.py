class Note:
    """
        Represents a note that contains text and optional tags for categorization.

        Attributes:
            text (str): The main content of the note.
            tags (list of str): A list of tags associated with the note.
    """

    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags if tags else []

    def __str__(self):
        return f"Tags: ({self.tags}), Note: {self.text}"
