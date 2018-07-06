from gpiozero import Motor, Button

from .settings import DEBUG


# Motor Initializations
syringe1 = Motor(SYRINGE1_FWD_PIN, SYRINGE1_REV_PIN)
syringe2 = Motor(SYRINGE2_FWD_PIN, SYRINGE2_REV_PIN)
syringe1.stop()
syringe2.stop()
syringe_array = [syringe1, syringe2]

syringe1_fwd_stop_switch = Button(SYRINGE1_FWD_STOP_PIN)
syringe1_rev_stop_switch = Button(SYRINGE1_REV_STOP_PIN)
syringe2_fwd_stop_switch = Button(SYRINGE2_FWD_STOP_PIN)
syringe2_rev_stop_switch = Button(SYRINGE2_REV_STOP_PIN)
syringe1_fwd_stop_switch.when_pressed = stop_syringe1
syringe1_rev_stop_switch.when_pressed = stop_syringe1
syringe2_fwd_stop_switch.when_pressed = stop_syringe2
syringe2_rev_stop_switch.when_pressed = stop_syringe2

# Switch Initializations
def stop_syringe1(direction):
    syringe1.stop()
    syringes[0]['currentstate'] = "idle"


def stop_syringe2():
    syringe2.stop()
    syringes[1]['currentstate'] = "idle"


def depress_syringe(syringe):
    index = syringe['id'] - 1
    syringe_array[index].forward(0.3)


def retract_syringe(syringe):
    index = syringe['id'] - 1
    syringe_array[index].backward(0.3)


def stop_syringe(syringe):
    index = syringe['id'] - 1
    syringe_array[index].stop()

