from openhab import rule, Registry
from openhab.triggers import GroupStateUpdateTrigger, SystemStartlevelTrigger


@rule(triggers=[SystemStartlevelTrigger(100)])
class SystemStarted:
    def execute(self, module, input):
        Registry.getItem("DeadMansSwitch").sendCommand("STARTUP")


@rule(triggers=[])  # eigener Trigger je nach Anwendungsfall
class RuleThatChangesAGWatchItem:
    def execute(self, module, input):
        Registry.getItem("DeadMansSwitch").sendCommand("RULE")
        # Aktionen ausfuehren
        Registry.getItem("DeadMansSwitch").sendCommand("MANUAL")


@rule(triggers=[GroupStateUpdateTrigger("gWatchItems")])
class IsManuallyTriggered:
    def execute(self, module, input):
        if str(Registry.getItem("DeadMansSwitch").state) == "MANUAL":
            pass  # Element wurde manuell ausgeloest
