#!/usr/bin/python3
"""RESTful API actions for state
"""
from flask import Flask, make_response, jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import state_views
from markupsafe import escape


@state_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    '''Returns all the state object in the storage'''
    states = storage.all(State)
    result = []
    for state, value in states.items():
        result.append(value.to_dict())
    return jsonify(result), 200


@state_views.route("/states/<string:state_id>", methods=['GET'],
                   strict_slashes=False)
def get_state(state_id):
    '''Returns a state object based on an id'''
    states = storage.all(State)
    for k, value in states.items():
        if value.id == state_id:
            return jsonify(value.to_dict()), 200
    return abort(404)


@state_views.route("/states/<string:state_id>", methods=['DELETE'],
                   strict_slashes=False)
def delete_state(state_id):
    '''Deletes a state object based on state id'''
    states = storage.all(State)

    for k, v in states.items():
        if v.id == state_id:
            v.delete()
            storage.save()
            return jsonify({}), 200
    return abort(404)


@state_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    '''Creates a new state object'''
    if not request.get_json():
        return abort(400, description="Not a JSON")
    else:
        data = request.get_json()
    if 'name' not in data:
        return abort(400, description="Missing name")
    ''' Can't seem to get the way around the error messages'''
    name = data.get('name')
    state = State(name=name)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@state_views.route("/states/<string:state_id>", methods=['PUT'],
                   strict_slashes=False)
def update_state(state_id):
    '''Updates a state object'''
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    states = storage.all(State)
    for k, v in states.items():
        if v.id == state_id:
            v['name'] = request.get_json('name')
    storage.save()
    return jsonify(states), 200
    abort(404)
