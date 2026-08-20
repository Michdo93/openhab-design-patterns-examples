from datetime import datetime

from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger

GLSM_OFF = "0"
GLSM_TIMED_ON = "2"
GLSM_TIMED_BLINK = "3"


@rule(triggers=[
    ItemStateChangeTrigger("LeftGarageDoor", state="OPEN"),
    ItemStateChangeTrigger("RightGarageDoor", state="OPEN"),
])
class GLSMGarageDoorUpEventHandler:
    def execute(self, module, input):
        sunset = Registry.getItem("Sun_Set").getState()
        after_sunset = str(sunset) not in ("NULL", "UNDEF") and sunset.getZonedDateTime() < datetime.now().astimezone()
        state = str(Registry.getItem("GLSM").getState())

        if after_sunset and state in (GLSM_OFF, GLSM_TIMED_ON, GLSM_TIMED_BLINK):
            Registry.getItem("GLSM").postUpdate(GLSM_TIMED_ON)
            self.logger.info("Tor geoeffnet nach Sonnenuntergang -> Licht mit Timer an")
        else:
            self.logger.info("Tor geoeffnet, aber kein Trigger (vor Sonnenuntergang oder Licht bereits dauerhaft an)")
