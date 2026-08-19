from openhab import rule, Registry
from openhab.triggers import GroupStateChangeTrigger

from deferred import set_deferred, cancel_deferred


@rule(triggers=[GroupStateChangeTrigger("gDeferredAction")])
class TimerSetzen:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        item_name = event.getItemName()
        if not item_name.lower().endswith("_timer"):
            return

        raw_state = str(Registry.getItem(item_name).getState())
        if not raw_state or raw_state == "NULL":
            return

        target = item_name[: -len("_Timer")]
        set_deferred(target, raw_state)
        Registry.getItem(item_name).postUpdate("")


@rule(triggers=[GroupStateChangeTrigger("gDeferredAction")])
class TimerEntfernen:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return
        cancel_deferred(event.getItemName())
