#!/usr/bin/python3
"""RESTful API actions for place"""
from flask import Flask, make_response, jsonify, abort, request
from models.state import State
from models.city import City
from models import storage
from models.place import Place
from api.v1.views import city_views
from api.v1.views import place_views
from markupsafe import escape


@place_views.route("/cities/<string:city_id>/places", methods=['GET'],
                   strict_slashes=False)
def get_places(city_id):
    """Returns all the places with city_id object in the storage"""
    cities = storage.all(City)
    places = storage.all(Place)
    result = []
    city_found = False
    for value in cities.values():
        if value.id == city_id:
            state_found = True
            break
    if not city_found:
        abort(404)
    for value in places.values():
        if value.city_id == city_id:
            result.append(value.to_dict())
    if not result:
        abort(404)
    return jsonify(result), 200


@place_views.route("/places/<string:place_id>", methods=['GET'],
                   strict_slashes=False)
def get_place(place_id):
    """Returns a place object based on an id"""
    places = storage.all(Place)
    for value in places.values():
        if value.id == place_id:
            return jsonify(value.to_dict()), 200
    return abort(404)


@place_views.route("/places/<string:place_id>", methods=['DELETE'],
                   strict_slashes=False)
def delete_place(place_id):
    """Deletes a place object based on state id"""
    places = storage.all(Place)

    for value in places.values():
        if value.id == place_id:
            value.delete()
            storage.save()
            return jsonify({}), 200
    return abort(404)


@place_views.route("/cities/<string:city_id>/places", methods=['POST'],
                   strict_slashes=False)
def create_place(city_id):
    """Creates a new place object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    if 'name' not in data():
        abort(400, "Missing name")
    key = 'City.' + city_id
    cities = storage.all(City)
    city = cities.get(key)
    if not state:
        abort(404)
    data.update({"city_id": city_id})
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@place_views.route("/places/<string:place_id>", methods=['PUT'],
                   strict_slashes=False)
def update_place(place_id):
    """Updates a place object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    key = 'Place.' + place_id
    places = storage.all(Place)
    place = places.get(key)
    if not place:
        abort(404)
    for key, value in (request.get_json()).items():
        if key != 'id' and key != 'created_at' and key != 'updated_at' \
                and key != 'city_id' and key != "user_id":
            setattr(place, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
    abort(404)
