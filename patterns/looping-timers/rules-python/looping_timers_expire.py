from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger, ItemCommandTrigger


@rule(triggers=[ItemStateChangeTrigger("MotionSensor", state="ON")])
class CeilingFanControl:
    def execute(self, module, input):
        if str(Registry.getItem("CeilingFanTimer").state) != "ON":
            Registry.getItem("CeilingFanTimer").sendCommand("OFF")  # Timer starten


@rule(triggers=[ItemCommandTrigger("CeilingFanTimer", "OFF")])
class CeilingFanLoop:
    def execute(self, module, input):
        if str(Registry.getItem("vTimeOfDay").state) != "NIGHT":
            return

        new_state = "STAY"
        current = float(str(Registry.getItem("CurrentTemp").state))
        target = float(str(Registry.getItem("TargetTemp").state))
        if current > target:
            new_state = "ON"
        elif current < target - 1:
            new_state = "OFF"

        if new_state != "STAY" and str(Registry.getItem("Fan").state) != new_state:
            Registry.getItem("Fan").sendCommand(new_state)

        Registry.getItem("CeilingFanTimer").sendCommand("ON")
