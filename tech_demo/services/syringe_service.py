#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request
from gpiozero import Motor, Button

app = Flask(__name__)

# Set GPIO pins for motors and stop switches here
SYRINGE1_FWD_PIN = 5
SYRINGE1_REV_PIN = 6
SYRINGE2_FWD_PIN = 23
SYRINGE2_REV_PIN = 24

SYRINGE1_FWD_STOP_PIN = 17
SYRINGE1_REV_STOP_PIN = 27
SYRINGE2_FWD_STOP_PIN = 22
SYRINGE2_REV_STOP_PIN = 26


# Motor Initializations
syringe1 = Motor(SYRINGE1_FWD_PIN, SYRINGE1_REV_PIN)
syringe2 = Motor(SYRINGE2_FWD_PIN, SYRINGE2_REV_PIN)
syringe1.stop()
syringe2.stop()
syringe_array = [syringe1, syringe2]


# Switch Initializations
def stop_syringe1(direction):
    syringe1.stop()
    syringes[0]['currentstate'] = "idle"


def stop_syringe2():
    syringe2.stop()
    syringes[1]['currentstate'] = "idle"


syringe1_fwd_stop_switch = Button(SYRINGE1_FWD_STOP_PIN)
syringe1_rev_stop_switch = Button(SYRINGE1_REV_STOP_PIN)
syringe2_fwd_stop_switch = Button(SYRINGE2_FWD_STOP_PIN)
syringe2_rev_stop_switch = Button(SYRINGE2_REV_STOP_PIN)
syringe1_fwd_stop_switch.when_pressed = stop_syringe1
syringe1_rev_stop_switch.when_pressed = stop_syringe1
syringe2_fwd_stop_switch.when_pressed = stop_syringe2
syringe2_rev_stop_switch.when_pressed = stop_syringe2


syringes = [
    {
        'id': 1,
        'forward_gpiopin': SYRINGE1_FWD_PIN,
        'reverse_gpiopin': SYRINGE1_REV_PIN,
        'forward_stop_gpiopin': SYRINGE1_FWD_STOP_PIN,
        'reverse_stop_gpiopin': SYRINGE1_REV_STOP_PIN,
        'currentstate': 'idle'
    },
    {
        'id': 2,
        'forward_gpiopin': SYRINGE2_FWD_PIN,
        'reverse_gpiopin': SYRINGE2_REV_PIN,
        'forward_stop_gpiopin': SYRINGE2_FWD_STOP_PIN,
        'reverse_stop_gpiopin': SYRINGE2_REV_STOP_PIN,
        'currentstate': 'idle'
    }

]


def depress_syringe(syringe):
    index = syringe['id'] - 1
    syringe_array[index].forward(0.3)


def retract_syringe(syringe):
    index = syringe['id'] - 1
    syringe_array[index].backward(0.3)


def stop_syringe(syringe):
    index = syringe['id'] - 1
    syringe_array[index].stop()


# The API allows clients to change the state of a syringe motor, as long as it matches one of the following states
valid_syringe_states = {
    'idle',
    'depressing',
    'retracting'
}


# Retrieve list of all syringes and their properties
@app.route('/syringes', methods=['GET'])
def get_syringes():
    return jsonify({'syringes': syringes})


# Retrieve properties of one specific syringe
@app.route('/syringes/<int:syringe_id>', methods=['GET'])
def get_syringe(syringe_id):
    syringe = [syringe for syringe in syringes if syringe['id'] == syringe_id]
    if len(syringe) == 0:
        abort(404)
    return jsonify({'syringe': syringe[0]})


# Allow client to set the state of a syringe motor
@app.route('/syringes/<int:syringe_id>', methods=['PUT'])
def update_syringe(syringe_id):
    syringe = [syringe for syringe in syringes if syringe['id'] == syringe_id]
    if len(syringe) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'currentstate' in request.json and type(request.json['currentstate']) is not unicode:
        abort(400)
    if request.json.get('currentstate') not in valid_syringe_states:
        abort(400)
    if request.json.get('currentstate') == 'depressing':
        print "Depressing syringe " + str(syringe[0]['id'])
        depress_syringe(syringe[0])
    if request.json.get('currentstate') == 'retracting':
        print "Retracting syringe " + str(syringe[0]['id'])
        retract_syringe(syringe[0])
    if request.json.get('currentstate') == 'idle':
        print "Stopping syringe " + str(syringe[0]['id'])
        stop_syringe(syringe[0])
    syringe[0]['currentstate'] = request.json.get('currentstate', syringe[0]['currentstate'])
    return jsonify({'syringe': syringe[0]})


# For 404, the client will expect a JSON formatted error code
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    print "Starting..."
    app.run(debug=False, host="0.0.0.0", port=7010)
