from openhab import rule, Registry
from openhab.triggers import GroupStateChangeTrigger


@rule(triggers=[GroupStateChangeTrigger("MyGroup")])
class GroupApproach:
    def execute(self, module, input):
        members = Registry.getItem("MyGroup").getAllMembers()
        if any(str(i.getState()) == "NULL" for i in members):
            self.logger.warn("One of the Items is NULL")
            return
        on_count = sum(1 for i in members if str(i.getState()) == "ON")
        new_state = "ON" if on_count >= 2 else "OFF"
        Registry.getItem("Buzz").sendCommand(new_state)
        self.logger.info("on_count={} -> Buzz={}".format(on_count, new_state))
