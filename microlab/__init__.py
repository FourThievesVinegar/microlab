import time

from flask import Flask, jsonify
from flask_cors import CORS

#from microlab.services.heater import api, process
#from microlab.time import get_time


app = Flask(__name__)
CORS(app)


# TODO: use logger, not scattered prints
@app.route("/time", methods=["GET"])
def get_time():
    """
    Just a simple time fetcher, for synchronizing between processes, etc.
    """
    return jsonify({"time": time.time()})


# if __name__ == '__main__':
#     print("Starting...")
#     app.run(debug=True, host="0.0.0.0", port=7012)

