#!/usr/bin/python3
"""
writted a Class for  FileStorage
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


classes = {"BaseModel": BaseModel, "User": User, "State": State,
           "Place": Place, "City": City, "Amenity": Amenity, "Review": Review}


class FileStorage:
    """serialize instance to json file and deserialize json file to instance"""

    # string - path to the JSON file (ex: file.json)
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_obj = {}
        for key in self.__objects:
            json_obj[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w', encoding='UTF-8') as file:
            json.dump(json_obj, file)

    def reload(self):
        """deserializes the JSON file to __objects"""
        # only if the JSON file (__file_path) exists
        # otherwise, do nothing. If the file doesn’t exist
        #  no exception should be raised
        try:
            with open(self.__file_path, 'r', encoding='UTF-8') as file:
                jn = json.load(file)
            for key in jn:
                self.__objects[key] = classes[jn[key]["__class__"]](**jn[key])
        except FileNotFoundError:
            pass
