class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags if tags else []
