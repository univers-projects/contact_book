class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags if tags else []

    def __str__(self):
        return f"Tags: ({self.tags}), Note: {self.text}"
