DEBUG=True

# Set GPIO pins for motors and stop switches here
SYRINGE1_FWD_PIN = 5
SYRINGE1_REV_PIN = 6
SYRINGE2_FWD_PIN = 23
SYRINGE2_REV_PIN = 24

SYRINGE1_FWD_STOP_PIN = 17
SYRINGE1_REV_STOP_PIN = 27
SYRINGE2_FWD_STOP_PIN = 22
SYRINGE2_REV_STOP_PIN = 26

SYRINGES = {
    1: {
        'forward_gpiopin': SYRINGE1_FWD_PIN,
        'reverse_gpiopin': SYRINGE1_REV_PIN,
        'forward_stop_gpiopin': SYRINGE1_FWD_STOP_PIN,
        'reverse_stop_gpiopin': SYRINGE1_REV_STOP_PIN,
        'currentstate': 'idle'
    },
    2: {
        'forward_gpiopin': SYRINGE2_FWD_PIN,
        'reverse_gpiopin': SYRINGE2_REV_PIN,
        'forward_stop_gpiopin': SYRINGE2_FWD_STOP_PIN,
        'reverse_stop_gpiopin': SYRINGE2_REV_STOP_PIN,
        'currentstate': 'idle'
    }
}

# The API allows clients to change the state of a syringe
# motor, as long as it matches one of the following states
VALID_STATES = {
    'idle',
    'depressing',
    'retracting'
}

