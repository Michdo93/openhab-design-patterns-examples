import threading

from openhab import rule, Registry
from openhab.triggers import ItemStateUpdateTrigger


@rule(triggers=[ItemStateUpdateTrigger("MotionSensor1", "ON")])
class MotionDetected:
    def execute(self, module, input):
        if str(Registry.getItem("Light1").getState()) == "OFF":
            Registry.getItem("Light1").sendCommand("ON")
            self.logger.info("Motion detected - Light1 switched on (10 min timer)")

            def turn_off():
                Registry.getItem("Light1").sendCommand("OFF")

            threading.Timer(10 * 60, turn_off).start()
        else:
            self.logger.info("Motion detected, but Light1 was already on")
