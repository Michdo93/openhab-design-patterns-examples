from openhab import rule, logger
from openhab.triggers import ItemCommandTrigger, ItemStateChangeTrigger

from supervision import supervise_state, cancel_supervision

T_RB_SECONDS = 30


def alert(item_name, expected_state):
    logger.warn(item_name + " hat den Zustand " + expected_state + " nicht erreicht")
    # z. B. Benachrichtigung senden


@rule(triggers=[ItemCommandTrigger("MySwitch")])
class MQTTStateSupervision:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        expected_state = str(event.getItemCommand())
        item_name = event.getItemName()
        logger.info(item_name + ": Ueberwachung gestartet, erwarte " + expected_state + " innerhalb " + str(T_RB_SECONDS) + "s")
        supervise_state(item_name, expected_state, alert, T_RB_SECONDS)


@rule(triggers=[ItemStateChangeTrigger("MySwitch")])
class MQTTStateUpdate:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        item_name = event.getItemName()
        logger.info(item_name + ": Zustand hat sich geaendert, Ueberwachung wird abgebrochen")
        cancel_supervision(item_name)
