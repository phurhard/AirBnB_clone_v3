#!/usr/bin/python3
""" Test the get method"""
from models import storage
from models.state import State
from models.place import Place
from models.base_model import BaseModel
'''
first_state_id = list(storage.all(State).values())[0].id
print("First State id: {}\n".format(first_state_id))
print("First State: {}\n".format(storage.get(State, first_state_id)))
print("All State: {}\n".format(storage.all(State)))
print("All Objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))
'''
new = Place()
print(new)
print(new.__dict__)
