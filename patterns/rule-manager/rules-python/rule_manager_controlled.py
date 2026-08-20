from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger


@rule(uid="example_rule_uid", name="ExampleRule (kontrollierte Ausfuehrung)",
      triggers=[ItemCommandTrigger("DummyExecTrigger")])
class ExampleRule:
    def execute(self, module, input):
        Registry.getItem("isRunningExampleRule").sendCommand("ON")

        if str(Registry.getItem("isRunningExampleRule").getState()) == "ON":
            self.logger.info("Teil 1 der Regel wird ausgefuehrt")
        else:
            self.logger.info("Teil 1: Aenderungen rueckgaengig gemacht (Abbruch erkannt)")

        if str(Registry.getItem("isRunningExampleRule").getState()) == "ON":
            self.logger.info("Teil 2 der Regel wird ausgefuehrt")
        else:
            self.logger.info("Teil 2: Aenderungen rueckgaengig gemacht (Abbruch erkannt)")

        Registry.getItem("isRunningExampleRule").sendCommand("OFF")
