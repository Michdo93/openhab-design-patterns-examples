import threading

from openhab import rule, Registry, logger
from openhab.actions import NotificationAction
from openhab.triggers import ItemStateChangeTrigger

MAX_RETRIES = 5
INITIAL_INTERVAL = 5
MAX_INTERVAL = 60


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


def send_command_with_backoff(item_name, command, retries=0, interval=INITIAL_INTERVAL):
    try:
        Registry.getItem(item_name).sendCommand(command)
        logger.info("Command '{}' sent to {} successfully!".format(command, item_name))
    except Exception as e:
        retries += 1
        logger.warn("Failed attempt #{} for {}: {}".format(retries, item_name, e))
        if retries < MAX_RETRIES:
            next_interval = min(interval * 2, MAX_INTERVAL)
            logger.info("Next attempt in {} seconds".format(next_interval))
            threading.Timer(
                next_interval, send_command_with_backoff, args=(item_name, command, retries, next_interval)
            ).start()
        else:
            logger.error("Maximum number of attempts for {} reached!".format(item_name))
            send_alert(item_name + " could not be switched ON")


@rule(triggers=[ItemStateChangeTrigger("SomeTrigger", state="ON")])
class GracefulRetryActionWithBackoff:
    def execute(self, module, input):
        send_command_with_backoff("LightSwitch", "ON")
