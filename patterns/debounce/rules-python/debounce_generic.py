import threading

from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger

timers = {}


@rule(triggers=[
    ItemStateChangeTrigger("Person1_PresenceSensors"),
    ItemStateChangeTrigger("Person2_PresenceSensors"),
])
class PresenceDetectionDebounce:
    def execute(self, module, input):
        item_name = input["itemName"]
        triggering_item = Registry.getItem(item_name)

        if item_name in timers:
            timers[item_name].cancel()

        delay = 0 if str(triggering_item.state) == "ON" else 2 * 60

        def on_expire(name=item_name, item=triggering_item):
            proxy_name = name.split("_")[0] + "_Present"
            proxy_item = Registry.getItem(proxy_name)
            if str(proxy_item.state) != str(item.state):
                proxy_item.sendCommand(item.state)
            del timers[name]

        t = threading.Timer(delay, on_expire)
        t.start()
        timers[item_name] = t
