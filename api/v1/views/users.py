#!/usr/bin/python3
"""RESTful API actions for state
"""
from flask import Flask, make_response, jsonify, abort, request
from models.user import User
from models import storage
from markupsafe import escape
from api.v1.views import user_views


@user_views.route("/users", methods=['GET'], strict_slashes=False)
def get_user():
    '''Returns all the users  object in the storage'''
    users = storage.all(User)
    result = []
    for value in users.values():
        result.append(value.to_dict())
    return jsonify(result), 200
    abort(404)


@user_views.route("/users/<string:user_id>", methods=['GET'],
                  strict_slashes=False)
def get_user_by_id(user_id):
    '''Returns a user object based on an id'''
    users = storage.all(User)
    for value in users.values():
        if value.id == user_id:
            return jsonify(value.to_dict()), 200
    return abort(404)


@user_views.route("/users/<string:user_id>", methods=['DELETE'],
                  strict_slashes=False)
def delete_user(user_id):
    '''Deletes a user object based on state id'''
    users = storage.all(User)

    for value in users.values():
        if value.id == user_id:
            value.delete()
            storage.save()
            return jsonify({}), 200
    return abort(404)


@user_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    '''Creates a new user object'''
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")
    new_user = Amenity(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@user_views.route("/users/<string:user_id>", methods=['PUT'],
                  strict_slashes=False)
def update_user(user_id):
    '''Updates a user object'''
    if not request.get_json():
        abort(400, "Not a JSON")
    key = 'User.' + amenity_id
    users = storage.all(User)
    user = users.get(key)
    if not user:
        abort(404)
    for key, value in (request.get_json()).items():
        if key != 'id' and key != 'created_at' and key != 'updated_at'\
                and key != 'email':
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
    abort(404)
