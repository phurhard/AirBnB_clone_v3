#!/usr/bin/python3
"""RESTful API actions for state
"""
from flask import Flask, make_response, jsonify, abort, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import city_views
from markupsafe import escape


@city_views.route("/states/<string:state_id>/cities", methods=['GET'],
                  strict_slashes=False)
def get_cities(state_id):
    '''Returns all the cities with state_id object in the storage'''
    cities = storage.all(City)
    states = storage.all(State)
    state_found = any(value.id == state_id for value in states.values())
    if not state_found:
        abort(404)
    result = [
        value.to_dict()
        for value in cities.values()
        if value.state_id == state_id
    ]
    return jsonify(result), 200


@city_views.route("/cities/<string:city_id>", methods=['GET'],
                  strict_slashes=False)
def get_city(city_id):
    '''Returns a city object based on an id'''
    cities = storage.all(City)
    for value in cities.values():
        if value.id == city_id:
            return jsonify(value.to_dict()), 200
    return abort(404)


@city_views.route("/cities/<string:city_id>", methods=['DELETE'],
                  strict_slashes=False)
def delete_city(city_id):
    '''Deletes a city object based on state id'''
    cities = storage.all(City)

    for value in cities.values():
        if value.id == city_id:
            value.delete()
            storage.save()
            return jsonify({}), 200
    return abort(404)


@city_views.route("/states/<string:state_id>/cities", methods=['POST'],
                  strict_slashes=False)
def create_city(state_id):
    '''Creates a new state object'''
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, "Missing name")
    key = f'State.{state_id}'
    states = storage.all(State)
    state = states.get(key)
    if not state:
        abort(404)
    data.update({"state_id": state_id})
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@city_views.route("/cities/<string:city_id>", methods=['PUT'],
                  strict_slashes=False)
def update_city(city_id):
    '''Updates a city object'''
    if not request.get_json():
        abort(400, "Not a JSON")
    key = f'City.{city_id}'
    cities = storage.all(City)
    city = cities.get(key)
    if not city:
        abort(404)
    for key, value in (request.get_json()).items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
