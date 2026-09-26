import threading

from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger

debounce_timer = None


@rule(triggers=[ItemStateChangeTrigger("motionSensor")])
class DebouncedMotionSensor:
    def execute(self, module, input):
        global debounce_timer

        if debounce_timer is None:
            self.logger.info("Motion detected - turning light on")
            Registry.getItem("light").sendCommand("ON")

            def reset_timer():
                global debounce_timer
                debounce_timer = None
                self.logger.info("Debounce finished - new events possible")

            debounce_timer = threading.Timer(2, reset_timer)
            debounce_timer.start()
        else:
            self.logger.info("Event ignored - timer still running")
