from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("DayNight", state="DAY", previous_state="NIGHT")])
class RolladenNachSonnenaufgangOeffnen:
    def execute(self, module, input):
        Registry.getItem("LoungeBlind_Timer").sendCommand("+15m->UP")
