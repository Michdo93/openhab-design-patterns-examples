from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("vTimeOfDay")])
class SetLightsBasedOnTimeOfDay:
    def execute(self, module, input):
        Registry.getItem("gLights_WEATHER_OVERRIDE").postUpdate("OFF")

        time_of_day = str(Registry.getItem("vTimeOfDay").state)

        off_group = next(
            (g for g in Registry.getItem("gLights_OFF").members if g.name == "gLights_OFF_" + time_of_day),
            None,
        )
        if off_group:
            for light in off_group.members:
                if str(light.state) != "OFF":
                    light.sendCommand("OFF")

        on_group = next(
            (g for g in Registry.getItem("gLights_ON").members if g.name == "gLights_ON_" + time_of_day),
            None,
        )
        if on_group:
            for light in on_group.members:
                if str(light.state) != "ON":
                    light.sendCommand("ON")
