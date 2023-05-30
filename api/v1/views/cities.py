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
    result = []
    state_found = False
    for value in states.values():
        if value.id == state_id:
            state_found = True
            break
    if not state_found:
        abort(404)
    for value in cities.values():
        if value.state_id == state_id:
            result.append(value.to_dict())
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
    temp = none
    states = storage.all(State)
    for value in states.values():
        if value.id == state_id:
            temp = value
            break
    if not temp:
        abort(404)
    name = data.get('name')
    state = City(name=name, state_id=state_id)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@city_views.route("/cities/<string:city_id>", methods=['PUT'],
                  strict_slashes=False)
def update_city(city_id):
    '''Updates a state object'''
    if not request.get_json():
        abort(400, "Not a JSON")
    cities = storage.all(City)
    for value in cities.values():
        if value.id == city_id:
            value['name'] = request.get_json('name')
    storage.save()
    return jsonify(cities), 200
    abort(404)
