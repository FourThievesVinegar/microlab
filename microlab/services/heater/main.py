#!/usr/bin/env python
import glob
import time
import threading

from app import app
from flask import Flask, jsonify, abort, make_response, request
from gpiozero import OutputDevice
#import uwsgidecorators

from .common import read_temp
from .settings import (
    HEATER_GPIO_PIN, HEATERS, VALID_STATES, BASE_DIR,
    DEVICE_FOLDER, DEVICE_FILE,
)

heater_dev = OutputDevice(HEATER_GPIO_PIN)
heater_dev.off()


def set_heater_operation(heater, operation):
    if operation == "off":
        heater_dev.off()
        heater["currentoperation"] = "idle"
    elif operation == "on":
        heater_dev.on()
        heater["currentoperation"] = "heating"
    else:
        raise NotImplementedError("Bad heater operation: %s"  operation)


def set_heater_state(heater, state):
    if state == "disabled":
        set_heater_operation("off")
    heater["currentstate"] = state


# TODO: extract this out to a persistent service
#@uwsgidecorators.postfork
#@uwsgidecorators.thread
def heater_update():
    while True:
        # First update temp reading
        HEATERS[0]['currenttemp'] = read_temp()

        if HEATERS[0]['currentstate'] == 'enabled':
            if HEATERS[0]['currenttemp'] < HEATERS[0]['settemp'] and HEATERS[0]['currentoperation'] is not 'heating':
                set_heater_operation("on")
            elif HEATERS[0]['currenttemp'] >= HEATERS[0]['settemp'] and HEATERS[0]['currentoperation'] is not 'idle':
                set_heater_operation("off")


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

    # TODO: Do this only in live mode, not test mode
    heater["settemp"] = settemp
    set_heater_state(heater, currentstate)
    # Do this in test mode
    heater["currentstate"] = currentstate

    print("SET: Heater: %s, temp: %s, state: %s" % (
        heater_id, currentstate, settemp))

    return jsonify({"heater": heater})


# For 404, the client will expect a JSON formatted error code
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

