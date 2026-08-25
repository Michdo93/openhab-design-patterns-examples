import threading

from openhab import rule, Registry, logger
from openhab.triggers import ItemStateChangeTrigger

ceiling_timer = None


def loop():
    global ceiling_timer
    if str(Registry.getItem("vTimeOfDay").getState()) == "NIGHT":
        current_state = str(Registry.getItem("CurrentTemp").getState())
        target_state = str(Registry.getItem("TargetTemp").getState())

        if current_state not in ("NULL", "UNDEF") and target_state not in ("NULL", "UNDEF"):
            new_state = "STAY"
            current = float(current_state)
            target = float(target_state)
            if current > target:
                new_state = "ON"
            elif current < target - 1:
                new_state = "OFF"

            if new_state != "STAY" and str(Registry.getItem("Fan").getState()) != new_state:
                Registry.getItem("Fan").sendCommand(new_state)
                logger.info("Fan -> " + new_state)

        ceiling_timer = threading.Timer(60, loop)
        ceiling_timer.start()
    else:
        ceiling_timer = None


@rule(triggers=[ItemStateChangeTrigger("MotionSensor", state="ON")])
class CeilingFanControl:
    def execute(self, module, input):
        global ceiling_timer
        if ceiling_timer is not None:
            return
        self.logger.info("Schleife gestartet")
        loop()
