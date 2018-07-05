import glob
import time
import threading

from flask import jsonify, abort, make_response, request
# from gpiozero import OutputDevice

from microlab import app
from microlab.services.heater.control import read_temp, set_heater_state
from microlab.services.heater.settings import (
    HEATER_GPIO_PIN, HEATERS, VALID_STATES, BASE_DIR,
    DEVICE_FOLDER, DEVICE_FILE, DEBUG,
)


# Retrieve list of all heaters and their properties
@app.route('/heaters', methods=['GET'])
def get_heaters():
    return jsonify({'heaters': HEATERS})


# Retrieve properties of one specific heater
@app.route('/heaters/<int:heater_id>', methods=['GET'])
def get_heater(heater_id):
    heater = HEATERS.get(heater_id)
    if not heater:
        abort(404, "Invalid heater ID specified.")

    return jsonify({'heater': heater[0]})


# Allow client to set the state and set temp of the heater
@app.route('/heaters/<int:heater_id>', methods=['PUT'])
def update_heater(heater_id):
    if not request.json:
        abort(400, "No JSON PUT body passed.")

    heater = HEATERS.get(heater_id)
    if not heater:
        abort(404, "Invalid heater ID specified.")

    currentstate = request.json.get("currentstate")
    settemp = request.json.get("settemp")

    if not currentstate or not settemp:
        abort(400, "'currentstate' and 'settemp' required.")

    if currentstate not in VALID_STATES:
        abort(400, "Invalid 'currentstate' specified.")

    if type(settemp) != int:
        abort(400, "Invalid 'settemp' specified.")

    heater["settemp"] = settemp
    heater["currentstate"] = state
    if not DEBUG:
        set_heater_state(heater, currentstate)

    print("SET: Heater: %s, temp: %s, state: %s" % (
        heater_id, currentstate, settemp))

    return jsonify({"heater": heater})


# For 404, the client will expect a JSON formatted error code
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

