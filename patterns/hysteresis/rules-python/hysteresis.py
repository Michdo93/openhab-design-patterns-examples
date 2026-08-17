from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("MyTemp")])
class HeizungMitHysterese:
    def execute(self, module, input):
        temp = float(str(Registry.getItem("MyTemp").state))
        new_command = "STAY"

        if temp < 68:
            new_command = "ON"
        elif temp >= 70:
            new_command = "OFF"

        heater = Registry.getItem("MyHeater")
        if new_command != "STAY" and new_command != str(heater.state):
            heater.sendCommand(new_command)
