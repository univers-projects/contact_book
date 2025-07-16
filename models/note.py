class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags if tags else []

##### - json storage task - #####

def __str__(self):
       #доданий для зручного виводу (опційно)
       return f"Note: {self.text} | Tags: {', '.join(self.tags)}"


   def to_dict(self):
       #Серіалізує Note у словник
       return {
           "text": self.text,
           "tags": self.tags
       }


   @classmethod
   def from_dict(cls, data):
       #Створює Note з JSON-словника
       return cls(
           text=data["text"],
           tags=data.get("tags", [])
       )