from openhab import rule, Registry
from openhab.services import getService
from openhab.triggers import ItemStateChangeTrigger

rule_manager = getService("org.openhab.core.automation.RuleManager")


@rule(triggers=[ItemStateChangeTrigger("exampleRule")])
class EnableDisableExampleRule:
    def execute(self, module, input):
        enabled = str(Registry.getItem("exampleRule").getState()) == "ON"
        rule_manager.setEnabled("example_rule_uid", enabled)
        self.logger.info("example_rule_uid enabled=" + str(enabled))
