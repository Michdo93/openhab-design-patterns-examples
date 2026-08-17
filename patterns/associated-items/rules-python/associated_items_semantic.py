from openhab import rule, Registry
from openhab.actions import Semantics
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("SomeSensor")])
class SensorHatEinUpdate:
    def execute(self, module, input):
        sensor = Registry.getItem("SomeSensor")
        equipment = Semantics.getEquipment(sensor)

        # Ansatz: Equipment-Name
        by_name = Registry.getItem(equipment.name + "_Status")

        # Ansatz: Item-Typ
        by_type = next((i for i in equipment.members if i.type == "Switch"), None)

        # Ansatz: Item-Tag
        by_tag = next((i for i in equipment.members if "Status" in i.tags), None)

        # Ansatz: mehrere Kriterien
        by_multi = next(
            (i for i in equipment.members if "Status" in i.tags and i.name.endswith("_Status")),
            None,
        )

        by_name.postUpdate(sensor.state)
