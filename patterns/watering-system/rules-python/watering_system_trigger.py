from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("SomeCondition", state="ON")])
class StartZone1Watering:
    def execute(self, module, input):
        Registry.getItem("VT_Watering_Zone1").postUpdate("START")
