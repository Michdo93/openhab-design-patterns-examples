import threading

from openhab import rule, Registry, logger
from openhab.actions import NotificationAction
from openhab.triggers import ItemStateChangeTrigger

MAX_RETRIES = 5
INITIAL_INTERVAL = 5
MAX_INTERVAL = 60


def send_command_with_backoff(item_name, command, retries=0, interval=INITIAL_INTERVAL):
    try:
        Registry.getItem(item_name).sendCommand(command)
        logger.info("Command '{}' an {} erfolgreich gesendet!".format(command, item_name))
    except Exception as e:
        retries += 1
        logger.warn("Fehlversuch #{} fuer {}: {}".format(retries, item_name, e))
        if retries < MAX_RETRIES:
            next_interval = min(interval * 2, MAX_INTERVAL)
            logger.info("Naechster Versuch in {} Sekunden".format(next_interval))
            threading.Timer(
                next_interval, send_command_with_backoff, args=(item_name, command, retries, next_interval)
            ).start()
        else:
            logger.error("Maximale Anzahl an Versuchen fuer {} erreicht!".format(item_name))
            NotificationAction.sendNotification("admin@example.com", item_name + " konnte nicht eingeschaltet werden")


@rule(triggers=[ItemStateChangeTrigger("SomeTrigger", state="ON")])
class GracefulRetryActionWithBackoff:
    def execute(self, module, input):
        send_command_with_backoff("LightSwitch", "ON")
