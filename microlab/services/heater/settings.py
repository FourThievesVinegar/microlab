import glob

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

# For 1-wire temp sensor interface
BASE_DIR = '/sys/bus/w1/devices/'
DEVICE_FOLDER = glob.glob(base_dir + '28*')[0]
DEVICE_FILE = device_folder + '/w1_slave'


