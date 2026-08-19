from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[
    ItemStateChangeTrigger("VT_Notify_Info"),
    ItemStateChangeTrigger("VT_Notify_Warn"),
    ItemStateChangeTrigger("VT_Notify_Alert"),
])
class Benachrichtigungsservice:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        item_name = event.getItemName()
        message = str(Registry.getItem(item_name).getState())
        # Logik zum Versenden der Nachricht, z. B. per Mail oder Push-Notification
        self.logger.info("[" + item_name + "] " + message)
