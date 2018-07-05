from time import sleep

from uwsgidecorators import postfork, thread

from .control import read_temp, set_heater_operation


# TODO: extract this out to a persistent service
# we will need a shared database to do this properly
@postfork
@thread
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

