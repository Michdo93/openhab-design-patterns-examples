from openhab import rule, Registry
from openhab.triggers import GroupStateChangeTrigger

from deferred import set_deferred, cancel_deferred


@rule(triggers=[GroupStateChangeTrigger("gDeferredAction")])
class TimerSetzen:
    def execute(self, module, input):
        item_name = input["itemName"]
        if not item_name.lower().endswith("_timer"):
            return

        raw_state = str(Registry.getItem(item_name).state)
        if not raw_state:
            return

        target = item_name[: -len("_Timer")]
        set_deferred(target, raw_state)
        Registry.getItem(item_name).postUpdate("")


@rule(triggers=[GroupStateChangeTrigger("gDeferredAction")])
class TimerEntfernen:
    def execute(self, module, input):
        cancel_deferred(input["itemName"])
