from openhab import rule, Registry
from openhab.triggers import GroupStateUpdateTrigger, SystemStartlevelTrigger, ItemCommandTrigger


@rule(triggers=[SystemStartlevelTrigger(100)])
class SystemStarted:
    def execute(self, module, input):
        Registry.getItem("DeadMansSwitch").sendCommand("STARTUP")


@rule(triggers=[ItemCommandTrigger("SomeRuleTrigger", "ON")])
class RuleThatChangesAGWatchItem:
    def execute(self, module, input):
        Registry.getItem("DeadMansSwitch").sendCommand("RULE")
        # Aktionen ausführen
        Registry.getItem("WatchedItem1").sendCommand("ON")
        Registry.getItem("DeadMansSwitch").sendCommand("MANUAL")


@rule(triggers=[GroupStateUpdateTrigger("gWatchItems")])
class IsManuallyTriggered:
    def execute(self, module, input):
        if str(Registry.getItem("DeadMansSwitch").getState()) == "MANUAL":
            self.logger.info("Item was triggered manually")
        else:
            self.logger.info("Item was triggered by a rule (DeadMansSwitch=RULE)")
