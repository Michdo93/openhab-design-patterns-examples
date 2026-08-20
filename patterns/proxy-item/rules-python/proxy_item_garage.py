from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger


@rule(triggers=[
    ItemCommandTrigger("Large_Garagedoor_Opener"),
    ItemCommandTrigger("Small_Garagedoor_Opener"),
])
class GaragentorController:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        if (str(Registry.getItem("GarageControllerComputer").getState()) != "ON"
                or str(Registry.getItem("GarageControllerService").getState()) != "ON"):
            Registry.getItem("AlertItem").sendCommand("Garagentor-Controller offline!")

        item_name = event.getItemName()
        command = str(event.getItemCommand())
        linked_item_name = item_name + "_Linked"
        Registry.getItem(linked_item_name).sendCommand(command)
        self.logger.info(item_name + " -> " + linked_item_name + ": " + command)
