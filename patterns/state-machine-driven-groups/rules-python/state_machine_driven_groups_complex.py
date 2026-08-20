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
                setting_state = setting.getState()
                if str(setting_state) in ("NULL", "UNDEF"):
                    self.logger.warn(light.getName() + ": Sollwert fuer " + time_of_day + " noch nicht gesetzt")
                    continue
                light.sendCommand(str(setting_state))
                self.logger.info(light.getName() + " -> " + str(setting_state))
