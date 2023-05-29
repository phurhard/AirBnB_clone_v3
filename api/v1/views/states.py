#!/usr/bin/python3
'''RESTful API actions for state
'''
from flask import Flask, make_response, jsonify
from models.state import State
from models import storage
from api.v1.views import state_views

@state_views.route("/states")
def get_states():
    states = storage.all(State)
    result = [state for state in states]
    return jsonify(result), 200
