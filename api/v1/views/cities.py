#!/usr/bin/python3
'''RESTful API actions for state
'''
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
    result = []
    for value in cities.values():
        if value.state_id == state_id:
            result.append(value.to_dict())
    if not result:
        abort(404)
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
    temp = {}
    states = storage.all(State)
    for value in states.values():
        if value.id == state_id:
            temp.append(value)
    if not temp:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    city = {
            "name": data['name'],
            "state_id": state_id
            }
    state = City(**(city))
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
