#!/usr/bin/python3
"""RESTful API actions for state
"""
from flask import Flask, make_response, jsonify, abort, request
from models.state import State
from models.city import City
from models.amenity import Amenity
from models import storage
from api.v1.views import amenity_views
from markupsafe import escape
from api.v1.views import amenity_views


@amenity_views.route("/amenities", methods=['GET'],
                     strict_slashes=False)
def get_amenities():
    '''Returns all the amenities  object in the storage'''
    amenities = storage.all(Amenity)
    result = []
    for value in amenities.values():
        result.append(value.to_dict())
    return jsonify(result), 200
    abort(404)


@amenity_views.route("/amenities/<string:amenity_id>", methods=['GET'],
                     strict_slashes=False)
def get_amenity(amenity_id):
    '''Returns a amenity object based on an id'''
    amenities = storage.all(Amenity)
    for value in amenities.values():
        if value.id == amenity_id:
            return jsonify(value.to_dict()), 200
    return abort(404)


@amenity_views.route("/amenities/<string:amenity_id>", methods=['DELETE'],
                     strict_slashes=False)
def delete_amenity(amenity_id):
    '''Deletes a amenity object based on state id'''
    amenities = storage.all(Amenity)

    for value in amenities.values():
        if value.id == amenity_id:
            value.delete()
            storage.save()
            return jsonify({}), 200
    return abort(404)


@amenity_views.route("/amenities",
                     methods=['POST'], strict_slashes=False)
def create_amenity():
    '''Creates a new amenity object'''
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@amenity_views.route("/amenities/<string:amenity_id>", methods=['PUT'],
                     strict_slashes=False)
def update_amenity(amenity_id):
    '''Updates a amenity object'''
    if not request.get_json():
        abort(400, "Not a JSON")
    key = 'Amenity.' + amenity_id
    amenities = storage.all(Amenity)
    amenity = amenities.get(key)
    if not amenity:
        abort(404)
    for key, value in (request.get_json()).items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
    abort(404)
