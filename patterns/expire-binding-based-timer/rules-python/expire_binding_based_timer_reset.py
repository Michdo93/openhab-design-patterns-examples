from openhab import rule, Registry
from openhab.triggers import SystemStartlevelTrigger


@rule(
    name="Restart expire timers",
    description="Reactivates all expire timers after system start",
    triggers=[SystemStartlevelTrigger(100)],
)
class RestartExpireTimers:
    def execute(self, module, input):
        self.logger.info("Restarting expire timers")
        for timer in Registry.getItem("gResetExpire").getAllMembers():
            self.logger.info(timer.getName() + " -> " + str(timer.getState()))
            timer.sendCommand(str(timer.getState()))
