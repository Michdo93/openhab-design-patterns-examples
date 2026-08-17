import threading

from openhab import rule, Registry, logger
from openhab.actions import NotificationAction
from openhab.triggers import ItemStateChangeTrigger

MAX_RETRIES = 3
RETRY_INTERVAL = 10  # Sekunden


def send_command_with_retry(item_name, command, retries=0):
    try:
        Registry.getItem(item_name).sendCommand(command)
        logger.info("Command '{}' an {} erfolgreich gesendet!".format(command, item_name))
    except Exception as e:
        retries += 1
        logger.warn("Fehler beim Senden an {}, Versuch #{}".format(item_name, retries))
        if retries < MAX_RETRIES:
            threading.Timer(RETRY_INTERVAL, send_command_with_retry, args=(item_name, command, retries)).start()
        else:
            logger.error("Maximale Anzahl an Versuchen fuer {} erreicht!".format(item_name))
            NotificationAction.sendNotification("admin@example.com", item_name + " konnte nicht eingeschaltet werden")


@rule(triggers=[ItemStateChangeTrigger("SomeTrigger", state="ON")])
class GracefulRetryLightSwitch:
    def execute(self, module, input):
        send_command_with_retry("LightSwitch", "ON")
