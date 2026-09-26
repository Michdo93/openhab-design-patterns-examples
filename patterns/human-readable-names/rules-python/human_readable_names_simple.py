from openhab import rule, Registry
from openhab.actions import Transformation
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("MyItem")])
class HumanReadableNameSimple:
    def execute(self, module, input):
        name = Transformation.transform("MAP", "admin.map", "MyItem") or "MyItem"
        self.logger.info(name + " is now " + str(Registry.getItem("MyItem").getState()))
