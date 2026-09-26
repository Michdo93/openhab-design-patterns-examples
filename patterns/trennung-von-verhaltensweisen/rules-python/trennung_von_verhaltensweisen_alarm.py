from openhab import rule, logger
from openhab.actions import NotificationAction
from openhab.triggers import ItemCommandTrigger


@rule(triggers=[
    ItemCommandTrigger("Notification_Proxy_Info"),
    ItemCommandTrigger("Notification_Proxy_Alert"),
])
class SendMessage:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        item_name = event.getItemName()
        command = str(event.getItemCommand())

        try:
            if item_name == "Notification_Proxy_Info":
                if NotificationAction is not None:
                    NotificationAction.sendNotification("admin@example.com", command)
                logger.info("Info notification: " + command)
            else:
                if NotificationAction is not None:
                    NotificationAction.sendBroadcastNotification(command)
                logger.info("Alert notification: " + command)
        except Exception as ex:
            logger.warn("Cloud notification not available: " + str(ex))
