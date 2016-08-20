#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request
from gpiozero import OutputDevice
import glob
import time
import threading
import uwsgidecorators

app = Flask(__name__)

HEATER_GPIO_PIN = 16

# For 1-wire temp sensor interface
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

heaters = [{
    'id': 1,
    'heater_gpiopin': HEATER_GPIO_PIN,
    'currentstate': 'disabled',
    'currentoperation': 'idle',
    'currenttemp': 21,
    'settemp': 35
}]

heater_dev = OutputDevice(HEATER_GPIO_PIN)
heater_dev.off()

valid_heater_states = {
    'disabled',
    'enabled'
}


def set_heater_state(state):
    if state == "disabled":
        set_heater_operation("off")
    heaters[0]['currentstate'] = state
    print "Setting heater state to " + heaters[0]['currentstate']


def set_heater_operation(operation):
    if operation == "off":
        heater_dev.off()
        heaters[0]['currentoperation'] = 'idle'
    elif operation == "on":
        heater_dev.on()
        heaters[0]['currentoperation'] = 'heating'
    print "Setting heater to " + heaters[0]['currentoperation']


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


@uwsgidecorators.postfork
@uwsgidecorators.thread
def heater_update():
    while True:
        # First update temp reading
        heaters[0]['currenttemp'] = read_temp()

        if heaters[0]['currentstate'] == 'enabled':
            if heaters[0]['currenttemp'] < heaters[0]['settemp'] and heaters[0]['currentoperation'] is not 'heating':
                set_heater_operation("on")
            elif heaters[0]['currenttemp'] >= heaters[0]['settemp'] and heaters[0]['currentoperation'] is not 'idle':
                set_heater_operation("off")


# Retrieve list of all heaters and their properties
@app.route('/heaters', methods=['GET'])
def get_heaters():
    return jsonify({'heaters': heaters})


# Retrieve properties of one specific heater
@app.route('/heaters/<int:heater_id>', methods=['GET'])
def get_heater(heater_id):
    heater = [heater for heater in heaters if heater['id'] == heater_id]
    if len(heater) == 0:
        abort(404)
    return jsonify({'heater': heater[0]})


# Allow client to set the state and set temp of the heater
@app.route('/heaters/<int:heater_id>', methods=['PUT'])
def update_heater(heater_id):
    print str(request.data)
    heater = [heater for heater in heaters if heater['id'] == heater_id]
    if len(heater) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'currentstate' in request.json and type(request.json['currentstate']) is not unicode:
        abort(400)
    if 'settemp' in request.json and type(request.json['settemp']) is not int:
        abort(400)
    if 'currentstate' in request.json and request.json.get('currentstate') not in valid_heater_states:
        abort(400)
    if 'currentstate' in request.json:
        set_heater_state(request.json.get('currentstate', heater[0]['currentstate']))
    if 'settemp' in request.json:
        heater[0]['settemp'] = request.json.get('settemp', heater[0]['settemp'])
        print "Setting heater set temp to " + str(heater[0]['settemp'])
    return jsonify({'heater': heater[0]})


# For 404, the client will expect a JSON formatted error code
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    print "Starting..."
    app.run(debug=False, host="0.0.0.0", port=7012)
