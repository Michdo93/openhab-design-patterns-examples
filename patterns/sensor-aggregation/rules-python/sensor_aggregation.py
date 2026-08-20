from openhab import rule, Registry
from openhab.triggers import (
    GroupStateChangeTrigger,
    ItemCommandTrigger,
    SystemStartlevelTrigger,
)


@rule(triggers=[SystemStartlevelTrigger(100)])
class ResetVPresentToOffOnStartup:
    def execute(self, module, input):
        Registry.getItem("vPresent").sendCommand("OFF")
        for s in Registry.getItem("gPresent").getAllMembers():
            s.sendCommand("OFF")


@rule(triggers=[GroupStateChangeTrigger("gPresent")])
class APresenceSensorUpdated:
    def execute(self, module, input):
        count = float(str(Registry.getItem("gPresent").getState()))
        v_present = Registry.getItem("vPresent")
        t_present = Registry.getItem("tPresent")

        self.logger.info("gPresent changed to " + str(count))
        if count > 0 and (str(v_present.getState()) != "ON" or str(t_present.getState()) == "ON"):
            self.logger.info("Someone came home")
            if str(t_present.getState()) != "OFF":
                t_present.postUpdate("OFF")
            if str(v_present.getState()) != "ON":
                v_present.sendCommand("ON")
        elif count == 0 and str(v_present.getState()) != "OFF" and str(t_present.getState()) != "ON":
            self.logger.info("Everyone is away, setting timer")
            t_present.sendCommand("ON")


@rule(triggers=[ItemCommandTrigger("tPresent", "OFF")])
class PresentTimerExpiredNoOneIsHome:
    def execute(self, module, input):
        count = float(str(Registry.getItem("gPresent").getState()))
        if count == 0:
            self.logger.info("Everyone is away, setting house to away")
            Registry.getItem("vPresent").sendCommand("OFF")
        else:
            self.logger.warn("Presence Timer expired but gPresent is " + str(count))
