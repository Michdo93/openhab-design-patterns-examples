import threading

from openhab import rule, Registry, logger
from openhab.actions import Transformation
from openhab.triggers import GroupStateChangeTrigger

alert_timers = {}


def alert_timer_expired(item_name, name, orig_state):
    del alert_timers[item_name]
    item = Registry.getItem(item_name)
    if str(item.getState()) == orig_state:
        display_value = Transformation.transform("MAP", "admin.map", str(item.getState()))
        logger.info(name + " is now " + display_value)
        item.getMetadata().set("Alert", "alerted", {"alerted": "ON"})


@rule(
    name="Device online/offline",
    description="Track device online/offline status",
    tags=["admin"],
    triggers=[GroupStateChangeTrigger("gSensorStatus")],
)
class DeviceOnlineOffline:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        old_state = event.getOldItemState()
        if old_state is None:
            return

        item_name = event.getItemName()
        item = Registry.getItem(item_name)

        alert_meta = item.getMetadata().get("Alert")
        alerted = alert_meta.getConfiguration().get("alerted", "OFF") if alert_meta else "OFF"
        name_meta = item.getMetadata().get("name")
        name = name_meta.getValue() if name_meta else item_name

        if item_name in alert_timers:
            alert_timers[item_name].cancel()
            del alert_timers[item_name]
            return  # Flapping erkannt: laufenden Timer abbrechen, kein neuer Alert

        current_state = str(item.getState())
        if alerted == current_state:
            t = threading.Timer(60, alert_timer_expired, args=(item_name, name, current_state))
            t.start()
            alert_timers[item_name] = t
