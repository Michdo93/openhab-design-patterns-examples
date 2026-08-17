from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("vTimeOfDay")])
class SetLightsBasedOnTimeOfDay:
    def execute(self, module, input):
        time_of_day = str(Registry.getItem("vTimeOfDay").state)
        Registry.getItem("gLights_OFF_" + time_of_day).sendCommand("OFF")
        Registry.getItem("gLights_ON_" + time_of_day).sendCommand("ON")
