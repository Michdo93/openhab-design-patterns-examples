from openhab import rule
from openhab.triggers import GroupStateChangeTrigger


@rule(triggers=[GroupStateChangeTrigger("DeviceStatuses", state="UNDEF")])
class ASensorStoppedReporting:
    def execute(self, module, input):
        event = input.get("event")
        item_name = event.getItemName() if event else "unknown"
        self.logger.warn(item_name + " stopped reporting (UNDEF) - raise alert/notification")
        # Meldung oder Alarm auslösen
