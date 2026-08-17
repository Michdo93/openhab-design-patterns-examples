from datetime import datetime

from openhab import rule, Registry
from openhab.triggers import GenericCronTrigger


@rule(triggers=[GenericCronTrigger("0 0 18 ? * * *")])
class AdjustLightBrightnessBasedOnTimeOfDay:
    def execute(self, module, input):
        hour = datetime.now().hour
        if 18 <= hour < 22:
            Registry.getItem("Light1_Dimmer").sendCommand(80)  # Helligkeit auf 80%
        else:
            Registry.getItem("Light1_Dimmer").sendCommand(20)  # Helligkeit auf 20%
