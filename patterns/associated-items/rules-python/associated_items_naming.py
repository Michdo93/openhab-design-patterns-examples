from openhab import rule, Registry, logger
from openhab.triggers import GroupStateChangeTrigger


@rule(triggers=[GroupStateChangeTrigger("gSensors")])
class FindAssociatedItemViaNamingConvention:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        item_name = event.getItemName()

        # Status-Items selbst nicht weiterverarbeiten, sonst würde nach
        # "Sensor1_Status_Status" gesucht, das es nicht gibt
        if item_name.endswith("_Status"):
            return

        try:
            status_item = Registry.getItem(item_name + "_Status")
        except Exception:
            logger.warn("No associated status item found for " + item_name)
            return

        # Den tatsächlichen neuen Zustand des Sensors übernehmen,
        # statt ihn fest auf ON zu setzen
        new_state = event.getItemState()
        status_item.postUpdate(new_state)
        logger.info("{} -> {} = {}".format(item_name, status_item.getName(), new_state))
