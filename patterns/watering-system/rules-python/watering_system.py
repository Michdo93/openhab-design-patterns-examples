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
        zone = input["itemName"]
        duration = int(str(Registry.getItem("VT_Watering_Duration").state))
        relay_name = zone.replace("VT_Watering_", "") + "_Relay"

        if str(Registry.getItem(zone).state) == "START":
            self.logger.info("Starte Bewaesserung fuer Zone {} fuer {} Sekunden".format(zone, duration))
            Registry.getItem(relay_name).sendCommand("ON")

            def turn_off(z=zone, relay=relay_name):
                self.logger.info("Beende Bewaesserung fuer Zone " + z)
                Registry.getItem(relay).sendCommand("OFF")
                del watering_timers[z]

            t = threading.Timer(duration, turn_off)
            t.start()
            watering_timers[zone] = t
