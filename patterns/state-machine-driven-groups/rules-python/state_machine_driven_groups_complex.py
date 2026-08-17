from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("vTimeOfDay")])
class SetLightsBasedOnTimeOfDay:
    def execute(self, module, input):
        time_of_day = str(Registry.getItem("vTimeOfDay").state)

        for light in Registry.getItem("gLights").members:
            setting = next(
                (s for s in Registry.getItem("gSettings").members
                 if s.name == light.name + "_" + time_of_day),
                None,
            )
            if setting is not None:
                light.sendCommand(setting.state)
