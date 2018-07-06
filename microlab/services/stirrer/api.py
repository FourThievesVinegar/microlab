#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request

from microlab import app
from .settings import STIRRERS, VALID_STATES, DEBUG
from .control import set_stirrer_state


# Retrieve list of all stirrers and their properties
@app.route('/stirrers', methods=['GET'])
def get_stirrers():
    return jsonify({'stirrers': STIRRERS})


# Retrieve properties of one specific stirrer
@app.route('/stirrers/<int:stirrer_id>', methods=['GET'])
def get_stirrer(stirrer_id):
    stirrer = STIRRERS.get(stirrer_id)

    if not stirrer:
        abort(404, "Bad stirrer ID specified.")

    return jsonify({'stirrer': stirrer})


# Allow client to set the state of the stirrer motor
@app.route('/stirrers/<int:stirrer_id>', methods=['PUT'])
def update_stirrer(stirrer_id):
    stirrer = STIRRERS.get(stirrer_id)

    if not stirrer:
        abort(404, "Bad stirrer ID specified.")

    if not request.json:
        abort(400, "No JSON body provided.")

    currentstate = request.json.get("currentstate")
    if currentstate not in VALID_STATES:
        abort(400, "Invalid currentstate set %s" % currentstate)

    if not DEBUG:
        set_stirrer_state(currentstate)

    stirrer['currentstate'] = state

    return jsonify({'stirrer': stirrer})


# For 404, the client will expect a JSON formatted error code
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

