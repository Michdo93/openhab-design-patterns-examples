from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger

GLSM_ON = "1"
GLSM_OFF = "0"


@rule(triggers=[ItemStateChangeTrigger("GarageLightsProxy", state="ON")])
class GarageLightsCommandedOn:
    def execute(self, module, input):
        Registry.getItem("GLSM").postUpdate(GLSM_ON)


@rule(triggers=[ItemStateChangeTrigger("GarageLightsProxy", state="OFF")])
class GarageLightsCommandedOff:
    def execute(self, module, input):
        Registry.getItem("GLSM").postUpdate(GLSM_OFF)
