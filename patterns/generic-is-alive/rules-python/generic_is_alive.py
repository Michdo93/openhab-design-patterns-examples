from openhab import rule
from openhab.triggers import GroupStateChangeTrigger


@rule(triggers=[GroupStateChangeTrigger("DeviceStatuses", state="UNDEF")])
class ASensorStoppedReporting:
    def execute(self, module, input):
        event = input.get("event")
        item_name = event.getItemName() if event else "unbekannt"
        self.logger.warn(item_name + " meldet sich nicht mehr (UNDEF) - Alarm/Meldung ausloesen")
        # Meldung oder Alarm ausloesen
