from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger, ItemCommandTrigger


@rule(triggers=[ItemStateChangeTrigger("MotionSensor", state="ON")])
class CeilingFanControl:
    def execute(self, module, input):
        if str(Registry.getItem("CeilingFanTimer").getState()) != "ON":
            Registry.getItem("CeilingFanTimer").sendCommand("OFF")  # Timer starten


@rule(triggers=[ItemCommandTrigger("CeilingFanTimer", "OFF")])
class CeilingFanLoop:
    def execute(self, module, input):
        if str(Registry.getItem("vTimeOfDay").getState()) != "NIGHT":
            return

        current_state = str(Registry.getItem("CurrentTemp").getState())
        target_state = str(Registry.getItem("TargetTemp").getState())

        if current_state not in ("NULL", "UNDEF") and target_state not in ("NULL", "UNDEF"):
            new_state = "STAY"
            current = float(current_state)
            target = float(target_state)
            if current > target:
                new_state = "ON"
            elif current < target - 1:
                new_state = "OFF"

            if new_state != "STAY" and str(Registry.getItem("Fan").getState()) != new_state:
                Registry.getItem("Fan").sendCommand(new_state)

        Registry.getItem("CeilingFanTimer").sendCommand("ON")
