from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("GarageLightsProxy", state="ON")])
class GarageLightsCommandedOn:
    def execute(self, module, input):
        Registry.getItem("GLSM").postUpdate(GLSM_ON)


@rule(triggers=[ItemStateChangeTrigger("GarageLightsProxy", state="OFF")])
class GarageLightsCommandedOff:
    def execute(self, module, input):
        Registry.getItem("GLSM").postUpdate(GLSM_OFF)
