#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __path = "file.json"
    __objs = {}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objs

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        obj_cls_name = obj.__class__.__name__
        FileStorage.__objs["{}.{}".format(obj_cls_name, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        obj_dict = FileStorage.__objs
        obj_dict = {obj: obj_dict[obj].to_dict() for obj in obj_dict.keys()}
        with open(FileStorage.__path, "w") as p:
            json.dump(obj_dict, p)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__path) as p:
                obj_dict = json.load(p)
                for obj in obj_dict.values():
                    cls_name = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval(cls_name)(**obj))
        except FileNotFoundError:
            return