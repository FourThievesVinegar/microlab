from .settings import (
    HEATER_GPIO_PIN, HEATERS, VALID_STATES, BASE_DIR,
    DEVICE_FOLDER, DEVICE_FILE, DEBUG,
)


heater_dev = None
if not DEBUG:
    from gpiozero import OutputDevice
    heater_dev = OutputDevice(HEATER_GPIO_PIN)
    heater_dev.off()


def read_temp_raw():
    f = open(DEVICE_FILE, 'r')
    lines = f.readlines()
    f.close()
    return lines


# need to make this read a specific heater
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


def set_heater_operation(heater, operation):
    if DEBUG:
        return
    if operation == "off":
        heater_dev.off()
        heater["currentoperation"] = "idle"
    elif operation == "on":
        heater_dev.on()
        heater["currentoperation"] = "heating"
    else:
        raise NotImplementedError("Bad heater operation: %s" % operation)


def set_heater_state(heater, state):
    if state == "disabled":
        set_heater_operation("off")

# This will get ran as a Celery command
def heater_control(self):
    while True:
        # Take current temp reading
        # Calculate gradient, gaussians, derivatives, etc, per control algorithm
        # Control the heater element accordingly
        # Sleep/loop, etc

