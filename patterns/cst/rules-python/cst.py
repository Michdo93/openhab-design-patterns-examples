from datetime import datetime

from openhab import rule, Registry
from openhab.triggers import GroupStateChangeTrigger


@rule(triggers=[GroupStateChangeTrigger("gCST")])
class ConditionalSequenceTrigger:
    def execute(self, module, input):
        hour = datetime.now().hour
        motion_on = str(Registry.getItem("motionSensor").getState()) == "ON"
        presence_on = str(Registry.getItem("presenceSensor").getState()) == "ON"

        if motion_on and presence_on and 18 <= hour <= 22:
            self.logger.info("All conditions met - starting sequence")
            Registry.getItem("light").sendCommand("ON")
            # Weitere Aktionen in definierter Reihenfolge
        else:
            self.logger.info("Conditions not met - resetting sequence")
            Registry.getItem("light").sendCommand("OFF")
            # optional: alle Zwischenschritte abbrechen
