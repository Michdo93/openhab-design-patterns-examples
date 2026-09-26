import threading

from openhab import rule, Registry, logger
from openhab.actions import NotificationAction
from openhab.triggers import ItemStateChangeTrigger

MAX_RETRIES = 3
RETRY_INTERVAL = 10  # Sekunden


def send_alert(message):
    # Lokale, immer verfügbare Alternative (kein Zusatz-Add-on nötig)
    try:
        Registry.getItem("NotificationItem").postUpdate(message)
    except Exception as ex:
        logger.warn("Could not update NotificationItem: " + str(ex))

    # Cloud-Benachrichtigung nur, wenn der openHAB Cloud Connector installiert
    # und verbunden ist - sonst ist NotificationAction None
    try:
        if NotificationAction is not None:
            NotificationAction.sendNotification("admin@example.com", message)
    except Exception as ex:
        logger.warn("Cloud notification not available: " + str(ex))


def send_command_with_retry(item_name, command, retries=0):
    try:
        Registry.getItem(item_name).sendCommand(command)
        logger.info("Command '{}' sent to {} successfully!".format(command, item_name))
    except Exception as e:
        retries += 1
        logger.warn("Error while sending to {}, attempt #{}".format(item_name, retries))
        if retries < MAX_RETRIES:
            threading.Timer(RETRY_INTERVAL, send_command_with_retry, args=(item_name, command, retries)).start()
        else:
            logger.error("Maximum number of attempts for {} reached!".format(item_name))
            send_alert(item_name + " could not be switched ON")


@rule(triggers=[ItemStateChangeTrigger("SomeTrigger", state="ON")])
class GracefulRetryLightSwitch:
    def execute(self, module, input):
        send_command_with_retry("LightSwitch", "ON")
