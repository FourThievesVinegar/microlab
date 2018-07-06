# TODO: change this to flask debug
DEBUG=True

STIRRER_GPIO_PIN = 25

STIRRERS = {
    1: {
        'forward_gpiopin': STIRRER_GPIO_PIN,
        'currentstate': 'off'
    }
}

VALID_STATES = {
    'off',
    'on'
}

