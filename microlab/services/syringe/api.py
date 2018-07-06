from flask import jsonify, abort, make_response, request

from microlab import app

from .settings import SYRINGES, VALID_STATES, DEBUG


# Retrieve list of all syringes and their properties
@app.route('/syringes', methods=['GET'])
def get_syringes():
    return jsonify({'syringes': SYRINGES})


# Retrieve properties of one specific syringe
@app.route('/syringes/<int:syringe_id>', methods=['GET'])
def get_syringe(syringe_id):
    syringe = SYRINGES.get(syringe_id)
    if not syringe:
        abort(404, "Invalid syringe ID specified.")

    return jsonify({'syringe': syringe})


# Allow client to set the state of a syringe motor
@app.route('/syringes/<int:syringe_id>', methods=['PUT'])
def update_syringe(syringe_id):
    syringe = SYRINGES.get(syringe_id)
    if not syringe:
        abort(404, "Invalid syringe ID specified.")

    if not request.json:
        abort(400, "No JSON body supplied.")

    currentstate = request.json.get("currentstate")

    if not currentstate:
        abort(400, "'currentstate' required.")

    if currentstate not in VALID_STATES:
        abort(400, "Invalid currentstate specified.")

    if not DEBUG:
        if currentstate == 'depressing':
            depress_syringe(syringe[0])

        elif currentstate == 'retracting':
            retract_syringe(syringe[0])

        elif currentstate == 'idle':
            stop_syringe(syringe[0])

        else:
            raise NotImplementedError("Bad currentstate %s" % currentstate)

    syringe['currentstate'] = currentstate

    return jsonify({'syringe': syringe})


# For 404, the client will expect a JSON formatted error code
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

