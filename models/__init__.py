#!/usr/bin/python3
"""
 structure for a system with different models 
"""
from models.engine import file_storage
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity

allclasses = {"BaseModel": BaseModel,
              "User": User,
              "State": State,
              "City": City,
              "Place": Place,
              "Amenity": Amenity,
              "Review": Review}

storage = file_storage.FileStorage()
storage.reload()
