import threading

from openhab import rule, Registry
from openhab.triggers import ItemStateUpdateTrigger

GLSM_OFF = "0"
GLSM_ON = "1"
GLSM_TIMED_ON = "2"
GLSM_TIMED_BLINK = "3"

glsm_timer = None
glsm_lock = threading.Lock()


@rule(triggers=[ItemStateUpdateTrigger("GLSM")])
class GLSMGarageLightsStateMachineEventsHandler:
    def execute(self, module, input):
        global glsm_timer

        with glsm_lock:
            state = str(Registry.getItem("GLSM").state)

            if state in ("NULL", "UNDEF"):
                Registry.getItem("GarageLights").sendCommand("OFF")
                Registry.getItem("GLSM").postUpdate(GLSM_OFF)
            elif state == GLSM_OFF:
                Registry.getItem("GarageLights").sendCommand("OFF")
                if glsm_timer is not None:
                    glsm_timer.cancel()
                    glsm_timer = None
            elif state == GLSM_ON:
                Registry.getItem("GarageLights").sendCommand("ON")
                if glsm_timer is not None:
                    glsm_timer.cancel()
                    glsm_timer = None
            elif state == GLSM_TIMED_ON:
                Registry.getItem("GarageLights").sendCommand("ON")

                def to_blink():
                    Registry.getItem("GLSM").postUpdate(GLSM_TIMED_BLINK)

                glsm_timer = threading.Timer(5 * 60, to_blink)
                glsm_timer.start()
            elif state == GLSM_TIMED_BLINK:
                Registry.getItem("GarageLights").sendCommand("OFF")
                Registry.getItem("GarageLights").sendCommand("ON")

                def to_off():
                    Registry.getItem("GLSM").postUpdate(GLSM_OFF)

                glsm_timer = threading.Timer(60, to_off)
                glsm_timer.start()
