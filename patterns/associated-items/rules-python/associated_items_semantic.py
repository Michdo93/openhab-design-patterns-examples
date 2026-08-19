from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("SomeSensor")])
class SensorHatEinUpdate:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        sensor = Registry.getItem(event.getItemName())

        equipment = sensor.getSemantic().getEquipment()
        if not equipment:
            self.logger.warn("Kein Equipment fuer " + sensor.getName() + " gefunden")
            return

        members = equipment.getAllMembers()

        # Robuster Ansatz: Tag "Status" + Namenskonvention kombiniert,
        # unabhaengig davon, wie das Equipment selbst benannt ist
        status_item = next(
            (i for i in members if "Status" in i.getTags() and i.getName().endswith("_Status")),
            None,
        )

        if not status_item:
            self.logger.warn("Kein Status-Item im Equipment " + equipment.getName() + " gefunden")
            return

        status_item.postUpdate(sensor.getState())
        self.logger.info(
            "{} -> {} = {}".format(sensor.getName(), status_item.getName(), sensor.getState())
        )
