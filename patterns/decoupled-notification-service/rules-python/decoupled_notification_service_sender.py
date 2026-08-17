from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("SomeCondition", state="ON")])
class InfoNotification:
    def execute(self, module, input):
        Registry.getItem("VT_Notify_Info").postUpdate("Information: Zustand geaendert")
