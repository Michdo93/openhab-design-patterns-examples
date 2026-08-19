from openhab import rule, Registry
from openhab.actions import Semantic
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("SomeSensor")])
class SensorHatEinUpdate:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        sensor = Registry.getItem(event.getItemName())
        equipment = Semantic.getEquipment(sensor)
        if not equipment:
            self.logger.warn("Kein Equipment fuer " + sensor.getName() + " gefunden")
            return

        members = equipment.getAllMembers()

        # Ansatz: Equipment-Name
        by_name = Registry.getItem(equipment.getName() + "_Status")

        # Ansatz: Item-Typ
        by_type = next((i for i in members if i.getType() == "Switch"), None)

        # Ansatz: Item-Tag
        by_tag = next((i for i in members if "Status" in i.getTags()), None)

        # Ansatz: mehrere Kriterien
        by_multi = next(
            (i for i in members if "Status" in i.getTags() and i.getName().endswith("_Status")),
            None,
        )

        by_name.postUpdate(sensor.getState())
