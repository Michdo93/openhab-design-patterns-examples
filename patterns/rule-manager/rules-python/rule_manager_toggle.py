from openhab import rule, Registry
from openhab.services import getService
from openhab.triggers import ItemStateChangeTrigger

rule_manager = getService("org.openhab.core.automation.RuleManager")


@rule(triggers=[ItemStateChangeTrigger("exampleRule")])
class EnableDisableExampleRule:
    def execute(self, module, input):
        enabled = str(Registry.getItem("exampleRule").state) == "ON"
        rule_manager.setEnabled("example_rule_uid", enabled)
