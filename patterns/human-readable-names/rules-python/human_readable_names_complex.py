import threading

from openhab import rule, Registry
from openhab.actions import Transformation
from openhab.triggers import GroupStateChangeTrigger

alert_timers = {}


@rule(triggers=[GroupStateChangeTrigger("gSensorStatus")])
class StatusAlert:
    def execute(self, module, input):
        old_state = input.get("oldItemState")
        if old_state is None:
            return

        item_name = input["itemName"]
        if item_name in alert_timers:
            alert_timers[item_name].cancel()

        orig_state = str(Registry.getItem(item_name).state)

        def on_expire():
            del alert_timers[item_name]
            if str(Registry.getItem(item_name).state) == orig_state:
                name = Transformation.transform("MAP", "admin.map", item_name) or item_name
                state_name = Transformation.transform("MAP", "admin.map", orig_state) or orig_state

                self.logger.info(name + " ist jetzt " + state_name)
                Registry.getItem(item_name + "_Alerted").postUpdate("ON")

        t = threading.Timer(60, on_expire)
        t.start()
        alert_timers[item_name] = t
