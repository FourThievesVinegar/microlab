from .settings import DEBUG, STIRRER_GPIO_PIN


stirrer_dev = None
if not DEBUG:
    from gpiozero import OutputDevice
    stirrer_dev = OutputDevice(STIRRER_GPIO_PIN)
    stirrer_dev.off()


def set_stirrer_state(state):
    if not stirrer_dev:
        raise Exception("Stirrer in DEBUG mode")

    if state == "off":
        stirrer_dev.off()
    elif state == "on":
        stirrer_dev.on()
    else:
        raise NotImplementedError("Bad stirrer state: %s" % state)

