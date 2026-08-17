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
        expected_state = str(input["command"])
        supervise_state(input["itemName"], expected_state, alert, T_RB_SECONDS)


@rule(triggers=[ItemStateChangeTrigger("MySwitch")])
class MQTTStateUpdate:
    def execute(self, module, input):
        cancel_supervision(input["itemName"])
