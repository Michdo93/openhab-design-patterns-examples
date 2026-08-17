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
        for s in Registry.getItem("gPresent").members:
            s.sendCommand("OFF")


@rule(triggers=[GroupStateChangeTrigger("gPresent")])
class APresenceSensorUpdated:
    def execute(self, module, input):
        count = float(str(Registry.getItem("gPresent").state))
        v_present = Registry.getItem("vPresent")
        t_present = Registry.getItem("tPresent")

        self.logger.debug("gPresent changed to " + str(count))
        if count > 0 and (str(v_present.state) != "ON" or str(t_present.state) == "ON"):
            self.logger.debug("Someone came home")
            if str(t_present.state) != "OFF":
                t_present.postUpdate("OFF")
            if str(v_present.state) != "ON":
                v_present.sendCommand("ON")
        elif count == 0 and str(v_present.state) != "OFF" and str(t_present.state) != "ON":
            self.logger.debug("Everyone is away, setting timer")
            t_present.sendCommand("ON")


@rule(triggers=[ItemCommandTrigger("tPresent", "OFF")])
class PresentTimerExpiredNoOneIsHome:
    def execute(self, module, input):
        count = float(str(Registry.getItem("gPresent").state))
        if count == 0:
            self.logger.info("Everyone is away, setting house to away")
            Registry.getItem("vPresent").sendCommand("OFF")
        else:
            self.logger.warn("Presence Timer expired but gPresent is " + str(count))
