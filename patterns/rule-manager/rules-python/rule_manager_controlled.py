from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger


@rule(uid="example_rule_uid", name="ExampleRule (controlled execution)",
      triggers=[ItemCommandTrigger("DummyExecTrigger")])
class ExampleRule:
    def execute(self, module, input):
        Registry.getItem("isRunningExampleRule").sendCommand("ON")

        if str(Registry.getItem("isRunningExampleRule").getState()) == "ON":
            self.logger.info("Part 1 of the rule is running")
        else:
            self.logger.info("Part 1: changes reverted (cancellation detected)")

        if str(Registry.getItem("isRunningExampleRule").getState()) == "ON":
            self.logger.info("Part 2 of the rule is running")
        else:
            self.logger.info("Part 2: changes reverted (cancellation detected)")

        Registry.getItem("isRunningExampleRule").sendCommand("OFF")
