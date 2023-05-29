#!/usr/bin/python3
''' This is the first endpoint of my flask api
'''
# Import required libraries
import os
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views, state_views

# configure the host and port
host = os.getenv("HBNB_API_HOST", "0.0.0.0")
port = int(os.getenv("HBNB_API_PORT", 5000))

# Create the flask app and register the blueprint
app = Flask(__name__)
app.register_blueprint(app_views)
app.register_blueprint(state_views)


# Create a method to stop the service
@app.teardown_appcontext
def teardown(exception):
    '''This method handles the app.teardowncontext
    by calling the storage.close'''
    storage.close()

# Error handler
@app.errorhandler(404)
def not_found(error):
    '''Returns a json of error not found message'''
    return make_response(jsonify({"error": "Not found"}), 404)


# run the flask server
if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
