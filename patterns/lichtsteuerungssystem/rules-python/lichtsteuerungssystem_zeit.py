from openhab import rule, Registry
from openhab.triggers import GenericCronTrigger


@rule(triggers=[GenericCronTrigger("0 30 6 ? * * *")])
class AdjustLightLevelsBasedOnTime:
    def execute(self, module, input):
        Registry.getItem("PresetDimLevel").postUpdate(20)
        Registry.getItem("UpdateLightLevels").sendCommand("ON")
