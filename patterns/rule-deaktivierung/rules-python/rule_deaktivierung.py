from openhab import rule, Registry
from openhab.services import getService
from openhab.triggers import ItemStateChangeTrigger, SystemStartlevelTrigger

rule_manager = getService("org.openhab.core.automation.RuleManager")


@rule(
    name="Christmas Mode",
    description="Enable/disable rules based on the state of vChristmas",
    tags=["christmas"],
    triggers=[
        ItemStateChangeTrigger("vChristmas"),
        SystemStartlevelTrigger(100),
    ],
)
class ChristmasMode:
    def execute(self, module, input):
        christmas_on = str(Registry.getItem("vChristmas").state) == "ON"

        rule_manager.setEnabled("christmas_lights", christmas_on)
        rule_manager.setEnabled("mbr_humidifier", not christmas_on)
