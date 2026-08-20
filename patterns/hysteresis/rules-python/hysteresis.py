from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("MyTemp")])
class HeizungMitHysterese:
    def execute(self, module, input):
        temp = float(str(Registry.getItem("MyTemp").getState()))
        new_command = "STAY"

        if temp < 68:
            new_command = "ON"
        elif temp >= 70:
            new_command = "OFF"

        heater = Registry.getItem("MyHeater")
        if new_command != "STAY" and new_command != str(heater.getState()):
            heater.sendCommand(new_command)
            self.logger.info("Temp={} -> Heizung={}".format(temp, new_command))
        else:
            self.logger.info("Temp={} -> keine Aenderung (Hysterese-Bereich oder bereits im Zielzustand)".format(temp))
