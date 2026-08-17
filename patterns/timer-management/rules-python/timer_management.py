import threading

from openhab import rule, Registry
from openhab.triggers import GroupStateChangeTrigger

timers = {}


@rule(triggers=[GroupStateChangeTrigger("Doors")])
class AlertIfDoorOpen:
    def execute(self, module, input):
        item_name = input["itemName"]

        # Bestehenden Timer abbrechen
        if item_name in timers:
            timers[item_name].cancel()
            del timers[item_name]

        # Timer neu erstellen, wenn Tuer geoeffnet wurde
        state = Registry.getItem(item_name).state
        if str(state) == "OPEN":
            def alert(name=item_name):
                Registry.getItem("Alert").sendCommand(name + " is still open!")

            t = threading.Timer(60 * 60, alert)
            t.start()
            timers[item_name] = t
