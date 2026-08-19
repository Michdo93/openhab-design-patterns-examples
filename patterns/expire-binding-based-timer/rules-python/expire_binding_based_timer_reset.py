from openhab import rule, Registry
from openhab.triggers import SystemStartlevelTrigger


@rule(
    name="Expire-Timer neu starten",
    description="Aktiviert alle Expire-Timer nach Systemstart",
    triggers=[SystemStartlevelTrigger(100)],
)
class ExpireTimerNeuStarten:
    def execute(self, module, input):
        self.logger.info("Expire-Timer werden neu gestartet")
        for timer in Registry.getItem("gResetExpire").getAllMembers():
            self.logger.info(timer.getName() + " -> " + str(timer.getState()))
            timer.sendCommand(str(timer.getState()))
