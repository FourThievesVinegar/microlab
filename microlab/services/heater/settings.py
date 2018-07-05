import glob


# TODO: change this to flask debug
DEBUG=True

# Put into a global settings file or auto-discover/wizard
HEATER_GPIO_PIN = 16

# TODO: discover some of this automatically
HEATERS = {
    1: {
        'heater_gpiopin': HEATER_GPIO_PIN,
        'currentstate': 'disabled',
        'currentoperation': 'idle',
        'currenttemp': 21,
        'settemp': 35,
    }
}

VALID_STATES = {
    'disabled',
    'enabled',
}

BASE_DIR = None
DEVICE_FOLDER = None
DEVICE_FILE = None
# For 1-wire temp sensor interface
if not DEBUG:
    BASE_DIR = '/sys/bus/w1/devices/'
    DEVICE_FOLDER = glob.glob(BASE_DIR + '28*')[0]
    DEVICE_FILE = DEVICE_FOLDER + '/w1_slave'

