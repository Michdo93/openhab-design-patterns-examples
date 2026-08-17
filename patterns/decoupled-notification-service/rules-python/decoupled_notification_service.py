from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[
    ItemStateChangeTrigger("VT_Notify_Info"),
    ItemStateChangeTrigger("VT_Notify_Warn"),
    ItemStateChangeTrigger("VT_Notify_Alert"),
])
class Benachrichtigungsservice:
    def execute(self, module, input):
        item_name = input["itemName"]
        message = str(Registry.getItem(item_name).state)
        # Logik zum Versenden der Nachricht, z. B. per Mail oder Push-Notification
        self.logger.info("[" + item_name + "] " + message)
