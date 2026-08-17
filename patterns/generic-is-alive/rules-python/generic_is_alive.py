from openhab import rule
from openhab.triggers import GroupStateChangeTrigger


@rule(triggers=[GroupStateChangeTrigger("DeviceStatuses", state="UNDEF")])
class ASensorStoppedReporting:
    def execute(self, module, input):
        pass  # Meldung oder Alarm ausloesen
