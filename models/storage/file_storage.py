##### - json storage task - #####

import json
from models.contact import Contact
from models.note import Note


STORAGE_FILE = "data.json"


def save_data(data):
   #Зберігає список об'єктів (Contact, Note) у файл JSON.
   #Кожен об'єкт перетворюється у словник з полем type.
  
   serializable = []
   for obj in data:
       if isinstance(obj, Contact):
           serializable.append({"type": "Contact", "data": obj.to_dict()})
       elif isinstance(obj, Note):
           serializable.append({"type": "Note", "data": obj.to_dict()})
       else:
           raise ValueError(f"Unsupported object type: {type(obj)}")


   with open(STORAGE_FILE, "w", encoding="utf-8") as f:
       json.dump(serializable, f, indent=4)


def load_data():
   #Завантажує список об'єктів з JSON-файлу.
   #Відновлює екземпляри класів Contact та Note.
  
   try:
       with open(STORAGE_FILE, "r", encoding="utf-8") as f:
           raw_data = json.load(f)
   except (FileNotFoundError, json.JSONDecodeError):
       return []


   restored_objects = []
   for item in raw_data:
       type_ = item.get("type")
       data = item.get("data")


       if type_ == "Contact":
           restored_objects.append(Contact.from_dict(data))
       elif type_ == "Note":
           restored_objects.append(Note.from_dict(data))
       else:
           print(f"Невідомий тип об'єкта: {type_}")


   return restored_objects
