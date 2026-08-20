from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("vTimeOfDay")])
class SetLightsBasedOnTimeOfDay:
    def execute(self, module, input):
        Registry.getItem("gLights_WEATHER_OVERRIDE").postUpdate("OFF")

        time_of_day = str(Registry.getItem("vTimeOfDay").getState())

        off_group = next(
            (g for g in Registry.getItem("gLights_OFF").getMembers()
             if g.getName() == "gLights_OFF_" + time_of_day),
            None,
        )
        if off_group:
            for light in off_group.getMembers():
                if str(light.getState()) != "OFF":
                    light.sendCommand("OFF")

        on_group = next(
            (g for g in Registry.getItem("gLights_ON").getMembers()
             if g.getName() == "gLights_ON_" + time_of_day),
            None,
        )
        if on_group:
            for light in on_group.getMembers():
                if str(light.getState()) != "ON":
                    light.sendCommand("ON")

        self.logger.info("vTimeOfDay=" + time_of_day + " -> Lichter angepasst")
