#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

HEATER_GPIO_PIN = 16

heaters = [{
    'id': 1,
    'heater_gpiopin': HEATER_GPIO_PIN,
    'currentstate': 'disabled',
    'currentoperation': 'idle',
    'currenttemp': 21,
    'settemp': 35
}]


valid_heater_states = {
    'disabled',
    'enabled'
}


def set_heater_state(state):
    heaters[0]['currentstate'] = state
    print "Setting heater state to " + heaters[0]['currentstate']


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


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
