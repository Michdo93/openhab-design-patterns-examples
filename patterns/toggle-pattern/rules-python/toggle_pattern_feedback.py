from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger


@rule(triggers=[ItemCommandTrigger("mqttSwitchIn2", "OFF")])
class ToggleLampeMitFeedback:
    def execute(self, module, input):
        lamp = Registry.getItem("modbusSwitchOut1")
        if str(lamp.state) != "ON":
            lamp.sendCommand("ON")
        else:
            lamp.sendCommand("OFF")
        lamp.postUpdate(lamp.state)
