from openhab import rule, Registry
from openhab.triggers import GroupStateChangeTrigger


@rule(triggers=[GroupStateChangeTrigger("MyGroup")])
class GroupApproach:
    def execute(self, module, input):
        members = Registry.getItem("MyGroup").members
        if any(str(i.state) == "NULL" for i in members):
            self.logger.warn("One of the Items is NULL")
            return
        on_count = sum(1 for i in members if str(i.state) == "ON")
        Registry.getItem("Buzz").sendCommand("ON" if on_count >= 2 else "OFF")
