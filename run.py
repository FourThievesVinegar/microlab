#!/usr/bin/env python
from microlab import app
from microlab.services.heater import api
from microlab.services.stirrer import api
from microlab.services.syringe import api
from microlab import time


if __name__ == "__main__":
    app.run()

