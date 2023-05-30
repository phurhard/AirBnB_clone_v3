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
    amenity = {
            name: request.get_json('name'),
            description: request.get_json('description', NULL),
            number_rooms: request.get_json('number_rooms', 0),
            number_bathrooms: request.get_json('number_bathrooms', 0),
            max_guest: request.get_json('max_guest', 0),
            price_by_night: request.get_json('price_by_night', 0),
            latitude: request.get_json("latitude", NULL),
            longitude: request.get_json('longitude', NULL)
            }
    new_amenity = Amenity(**amenity)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@amenity_views.route("/amenities/<string:amenity_id>", methods=['PUT'],
                     strict_slashes=False)
def update_amenity(amenity_id):
    '''Updates a amenity object'''
    if not request.get_json():
        abort(400, "Not a JSON")
    amenities = storage.all(Amenity)
    for value in amenities.values():
        if value.id == amenity_id:
            value['name'] = request.get_json('name')
            value['description'] = request.get_json('description', NULL)
            value['number_rooms'] = request.get_json('number_rooms', 0)
            value['number_bathrooms'] = request.get_json(
                            'number_bathrooms', 0)
            value['max_guest'] = request.get_json('max_guest', 0)
            value['price_by_night'] = request.get_json('price_by_night',
                                                       0)
            value['latitude'] = request.get_json("latitude", NULL)
            value['longitude'] = request.get_json('longitude', NULL)
        storage.save()
        return jsonify(amenities), 200
    abort(404)
