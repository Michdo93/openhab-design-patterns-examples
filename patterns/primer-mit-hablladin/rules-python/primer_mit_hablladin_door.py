from datetime import datetime

from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[
    ItemStateChangeTrigger("LeftGarageDoor", state="OPEN"),
    ItemStateChangeTrigger("RightGarageDoor", state="OPEN"),
])
class GLSMGarageDoorUpEventHandler:
    def execute(self, module, input):
        sunset = Registry.getItem("Sun_Set").state
        after_sunset = str(sunset) != "NULL" and sunset.getZonedDateTime() < datetime.now().astimezone()
        state = str(Registry.getItem("GLSM").state)

        if after_sunset and state in (GLSM_OFF, GLSM_TIMED_ON, GLSM_TIMED_BLINK):
            Registry.getItem("GLSM").postUpdate(GLSM_TIMED_ON)
