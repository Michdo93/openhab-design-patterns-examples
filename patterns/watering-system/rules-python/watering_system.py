import threading

from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger

watering_timers = {}


@rule(triggers=[
    ItemStateChangeTrigger("VT_Watering_Zone1"),
    ItemStateChangeTrigger("VT_Watering_Zone2"),
])
class WateringService:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        zone = event.getItemName()
        duration_state = str(Registry.getItem("VT_Watering_Duration").getState())
        if duration_state in ("NULL", "UNDEF"):
            self.logger.warn("VT_Watering_Duration ist noch nicht gesetzt")
            return
        duration = int(duration_state)

        relay_name = zone.replace("VT_Watering_", "") + "_Relay"

        if str(Registry.getItem(zone).getState()) == "START":
            self.logger.info("Starte Bewaesserung fuer Zone {} fuer {} Sekunden".format(zone, duration))
            Registry.getItem(relay_name).sendCommand("ON")

            def turn_off(z=zone, relay=relay_name):
                self.logger.info("Beende Bewaesserung fuer Zone " + z)
                Registry.getItem(relay).sendCommand("OFF")
                del watering_timers[z]

            t = threading.Timer(duration, turn_off)
            t.start()
            watering_timers[zone] = t
