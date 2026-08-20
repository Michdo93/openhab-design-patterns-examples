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
        christmas_on = str(Registry.getItem("vChristmas").getState()) == "ON"

        rule_manager.setEnabled("christmas_lights", christmas_on)
        rule_manager.setEnabled("mbr_humidifier", not christmas_on)
        self.logger.info(
            "vChristmas={} -> christmas_lights enabled={}, mbr_humidifier enabled={}".format(
                christmas_on, christmas_on, not christmas_on
            )
        )
