import threading

from openhab import rule, Registry
from openhab.actions import Transformation
from openhab.triggers import GroupStateChangeTrigger

alert_timers = {}


def alert_timer_expired(item_name, name, orig_state):
    del alert_timers[item_name]
    item = Registry.getItem(item_name)
    if str(item.state) == orig_state:
        display_value = Transformation.transform("MAP", "admin.map", str(item.state))
        print(name + " is now " + display_value)
        item.getMetadata().set("Alert", "alerted", {"alerted": "ON"})


@rule(
    name="Device online/offline",
    description="Track device online/offline status",
    tags=["admin"],
    triggers=[GroupStateChangeTrigger("gSensorStatus")],
)
class DeviceOnlineOffline:
    def execute(self, module, input):
        old_state = input.get("oldItemState")
        if old_state is None:
            return

        item_name = input["itemName"]
        item = Registry.getItem(item_name)

        alert_meta = item.getMetadata().get("Alert")
        alerted = alert_meta.configuration.get("alerted", "OFF") if alert_meta else "OFF"
        name_meta = item.getMetadata().get(None)
        name = name_meta.value if name_meta else item_name

        if item_name in alert_timers:
            alert_timers[item_name].cancel()
            del alert_timers[item_name]
            return  # Flapping erkannt: laufenden Timer abbrechen, kein neuer Alert

        if alerted == str(item.state):
            t = threading.Timer(60, alert_timer_expired, args=(item_name, name, str(item.state)))
            t.start()
            alert_timers[item_name] = t
