from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger

PRESENT_TARGETS = {
    "Room1_Thermostat": 21,
    "Room2_Thermostat": 22,
}
AWAY_TARGETS = {
    "Room1_Thermostat": 17,
    "Room2_Thermostat": 18,
}


@rule(triggers=[ItemStateChangeTrigger("vPresent")])
class ZieltemperaturenAnwenden:
    def execute(self, module, input):
        targets = PRESENT_TARGETS if str(Registry.getItem("vPresent").state) == "ON" else AWAY_TARGETS
        for name, temp in targets.items():
            Registry.getItem(name).sendCommand(temp)
