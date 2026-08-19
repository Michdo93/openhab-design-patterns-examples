from openhab import rule, Registry
from openhab.triggers import GroupStateChangeTrigger


@rule(triggers=[GroupStateChangeTrigger("gSensors")])
class ZugehoerigesItemUeberNamenskonventionFinden:
    def execute(self, module, input):
        item_name = input["itemName"]
        status_item = Registry.getItem(item_name + "_Status")
        status_item.postUpdate("ON")
