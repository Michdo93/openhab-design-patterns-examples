from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("vTimeOfDay")])
class SetLightsBasedOnTimeOfDay:
    def execute(self, module, input):
        time_of_day = str(Registry.getItem("vTimeOfDay").getState())

        for light in Registry.getItem("gLights").getAllMembers():
            setting = next(
                (s for s in Registry.getItem("gSettings").getAllMembers()
                 if s.getName() == light.getName() + "_" + time_of_day),
                None,
            )
            if setting is not None:
                light.sendCommand(setting.getState())
                self.logger.info(light.getName() + " -> " + str(setting.getState()))
