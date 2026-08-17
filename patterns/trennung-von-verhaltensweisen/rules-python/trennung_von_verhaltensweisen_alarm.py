from openhab import rule
from openhab.actions import NotificationAction
from openhab.triggers import ItemCommandTrigger


@rule(triggers=[
    ItemCommandTrigger("Notification_Proxy_Info"),
    ItemCommandTrigger("Notification_Proxy_Alert"),
])
class SendMessage:
    def execute(self, module, input):
        item_name = input["itemName"]
        command = str(input["command"])

        if item_name == "Notification_Proxy_Info":
            NotificationAction.sendNotification("admin@example.com", command)
        else:
            NotificationAction.sendBroadcastNotification(command)
