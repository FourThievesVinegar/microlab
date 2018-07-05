#!/usr/bin/python
from app import app
from flask import Flask, jsonify, abort, make_response, request
from .settings import HEATER_GPIO_PIN, HEATERS, VALID_STATES


def set_heater_state(state):
    if state == "disabled":
        set_heater_operation("off")
    HEATERS[0]['currentstate'] = state


# Retrieve list of all heaters and their properties
@app.route('/heaters', methods=['GET'])
def get_heaters():
    return jsonify({'heaters': HEATERS})


# Retrieve properties of one specific heater
@app.route('/heaters/<int:heater_id>', methods=['GET'])
def get_heater(heater_id):
    heater = HEATERS.get(heater_id)
    if not heater:
        abort(404)
    return jsonify({'heater': heater})


# Allow client to set the state and set temp of the heater
@app.route('/heaters/<int:heater_id>', methods=['PUT'])
def update_heater(heater_id):
    heater = HEATERS.get(heater_id)

    if not heater or not request.json:
        abort(404, "Invalid heater ID specified.")

    currentstate = request.json.get("currentstate")
    settemp = request.json.get("settemp")

    if not currentstate or not settemp:
        abort(400, "'currentstate' and 'settemp' required.")

    if currentstate not in VALID_STATES:
        abort(400, "Invalid 'currentstate' specified.")

    if type(settemp) != int:
        abort(400, "Invalid 'settemp' specified.")

    heater["currentstate"] = currentstate
    heater["settemp"] = settemp

    print("SET: Heater: %s, temp: %s, state: %s" % (
        heater_id, currentstate, settemp))

    return jsonify({"heater": heater})


# For 404, the client will expect a JSON formatted error code
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found."}), 404)

