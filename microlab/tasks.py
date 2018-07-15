from time import sleep

from celery import Celery

from microlab.settings import AMPQ_PASS
from microlab.services.heater.control import (
    read_temp, set_heater_operation
)



app = Celery(
    'tasks',
    broker='pyamqp://microlab:%s@localhost:5672/microlab' % AMPQ_PASS
)


# TODO: turn this into a celery beat worker
@app.task
def heater_update():
    while True:
        # TODO: update each heater per HEATERS file, right now
        # we can only use one (the first)
        id = tuple(HEATERS.keys())[0]
        heater = HEATERS[id]
        print("Heater update ID %s" % id)
        heater['currenttemp'] = read_temp()

        currentstate = heater["currentstate"]
        currenttemp = heater["currenttemp"]
        settemp = heater["settemp"]
        currentop = heater["currentoperation"]

        if currentstate == "enabled":
            if currenttemp < settemp and currentop != "heating":
                set_heater_operation("on")
            elif currenttemp >= settemp and currentop != "idle":
                set_heater_operation("off")

        sleep(0.5)

