from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger


@rule(triggers=[
    ItemCommandTrigger("Large_Garagedoor_Opener"),
    ItemCommandTrigger("Small_Garagedoor_Opener"),
])
class GaragentorController:
    def execute(self, module, input):
        if (str(Registry.getItem("GarageControllerComputer").state) != "ON"
                or str(Registry.getItem("GarageControllerService").state) != "ON"):
            Registry.getItem("AlertItem").sendCommand("Garagentor-Controller offline!")

        linked_item_name = input["itemName"] + "_Linked"
        Registry.getItem(linked_item_name).sendCommand(input["command"])
