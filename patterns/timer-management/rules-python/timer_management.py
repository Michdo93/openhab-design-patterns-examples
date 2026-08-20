import threading

from openhab import rule, Registry
from openhab.triggers import GroupStateChangeTrigger

timers = {}


@rule(triggers=[GroupStateChangeTrigger("Doors")])
class AlertIfDoorOpen:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        item_name = event.getItemName()

        # Bestehenden Timer abbrechen
        if item_name in timers:
            timers[item_name].cancel()
            del timers[item_name]

        # Timer neu erstellen, wenn Tuer geoeffnet wurde
        state = Registry.getItem(item_name).getState()
        if str(state) == "OPEN":
            def alert(name=item_name):
                Registry.getItem("Alert").sendCommand(name + " is still open!")

            t = threading.Timer(60 * 60, alert)
            t.start()
            timers[item_name] = t
            self.logger.info(item_name + ": Timer gestartet (1h)")
        else:
            self.logger.info(item_name + ": geschlossen, kein Timer noetig")
