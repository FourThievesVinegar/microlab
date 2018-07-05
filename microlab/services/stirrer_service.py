#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request
from gpiozero import OutputDevice

app = Flask(__name__)

STIRRER_GPIO_PIN = 25


stirrers = [{
    'id': 1,
    'forward_gpiopin': STIRRER_GPIO_PIN,
    'currentstate': 'off'
}]


stirrer_dev = OutputDevice(STIRRER_GPIO_PIN)
stirrer_dev.off()


valid_stirrer_states = {
    'off',
    'on'
}


def set_stirrer_state(state):
    if state == "off":
        stirrer_dev.off()
    elif state == "on":
        stirrer_dev.on()
    stirrers[0]['currentstate'] = state
    print "Setting stirrer to " + stirrers[0]['currentstate']


# Retrieve list of all stirrers and their properties
@app.route('/stirrers', methods=['GET'])
def get_stirrers():
    return jsonify({'stirrers': stirrers})


# Retrieve properties of one specific stirrer
@app.route('/stirrers/<int:stirrer_id>', methods=['GET'])
def get_stirrer(stirrer_id):
    stirrer = [stirrer for stirrer in stirrers if stirrer['id'] == stirrer_id]
    if len(stirrer) == 0:
        abort(404)
    return jsonify({'stirrer': stirrer[0]})


# Allow client to set the state of the stirrer motor
@app.route('/stirrers/<int:stirrer_id>', methods=['PUT'])
def update_stirrer(stirrer_id):
    stirrer = [stirrer for stirrer in stirrers if stirrer['id'] == stirrer_id]
    if len(stirrer) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if request.json.get('currentstate') not in valid_stirrer_states:
        abort(400)
    set_stirrer_state(request.json.get('currentstate', stirrer[0]['currentstate']))
    return jsonify({'stirrer': stirrer[0]})


# For 404, the client will expect a JSON formatted error code
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    print "Starting..."
    app.run(debug=False, host="0.0.0.0", port=7011)
