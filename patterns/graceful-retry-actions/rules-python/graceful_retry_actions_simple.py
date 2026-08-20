import threading

from openhab import rule, Registry, logger
from openhab.actions import NotificationAction
from openhab.triggers import ItemStateChangeTrigger

MAX_RETRIES = 3
RETRY_INTERVAL = 10  # Sekunden


def send_alert(message):
    # Lokale, immer verfuegbare Alternative (kein Zusatz-Add-on noetig)
    try:
        Registry.getItem("NotificationItem").postUpdate(message)
    except Exception as ex:
        logger.warn("Konnte NotificationItem nicht aktualisieren: " + str(ex))

    # Cloud-Benachrichtigung nur, wenn der openHAB Cloud Connector installiert
    # und verbunden ist - sonst ist NotificationAction None
    try:
        if NotificationAction is not None:
            NotificationAction.sendNotification("admin@example.com", message)
    except Exception as ex:
        logger.warn("Cloud-Benachrichtigung nicht verfuegbar: " + str(ex))


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
            send_alert(item_name + " konnte nicht eingeschaltet werden")


@rule(triggers=[ItemStateChangeTrigger("SomeTrigger", state="ON")])
class GracefulRetryLightSwitch:
    def execute(self, module, input):
        send_command_with_retry("LightSwitch", "ON")
