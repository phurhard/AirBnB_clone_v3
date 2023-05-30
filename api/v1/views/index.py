#!/usr/bin/python3
""" Index view of the app
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User


@app_views.route('/status', strict_slashes=False)
def Status():
    '''Returns a JSON status of the route'''
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def Stats():
    '''Retrieves the number of each objects by type'''
    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
        })
