import threading

from openhab import rule, Registry
from openhab.triggers import GroupCommandTrigger

TIMEOUT_SECONDS = 5 * 60
timers = {}


@rule(triggers=[GroupCommandTrigger("gMotionDetectors", "ON")])
class AMotionDetectorTriggered:
    def execute(self, module, input):
        item_name = input["itemName"]

        if item_name in timers:
            timers[item_name].cancel()

        def turn_off(name=item_name):
            Registry.getItem(name).sendCommand("OFF")
            del timers[name]

        t = threading.Timer(TIMEOUT_SECONDS, turn_off)
        t.start()
        timers[item_name] = t
