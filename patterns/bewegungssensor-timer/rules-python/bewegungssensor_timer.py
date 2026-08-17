import threading

from openhab import rule, Registry
from openhab.triggers import ItemStateUpdateTrigger

occupancy_timer = None


def turn_off():
    global occupancy_timer
    Registry.getItem("MotionDetector1").sendCommand("OFF")
    occupancy_timer = None


@rule(triggers=[ItemStateUpdateTrigger("MotionDetector1", "ON")])
class MotionDetector1ReceivedOn:
    def execute(self, module, input):
        global occupancy_timer
        if occupancy_timer is not None:
            occupancy_timer.cancel()

        occupancy_timer = threading.Timer(5 * 60, turn_off)
        occupancy_timer.start()
