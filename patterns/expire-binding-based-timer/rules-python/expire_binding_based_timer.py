from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger


@rule(triggers=[ItemCommandTrigger("StartMyTimerTrigger", "ON")])
class ARuleThatStartsTheTimer:
    def execute(self, module, input):
        # Arbeitsschritte ausführen

        if str(Registry.getItem("MyTimer").getState()) == "ON":
            self.logger.info("Timer is already active - restarting")

        # Timer abbrechen
        Registry.getItem("MyTimer").postUpdate("OFF")

        # Timer starten
        Registry.getItem("MyTimer").sendCommand("ON")
        self.logger.info("MyTimer started (5 minutes)")


@rule(triggers=[ItemCommandTrigger("MyTimer", "OFF")])
class MyTimerExpired:
    def execute(self, module, input):
        self.logger.info("MyTimer expired - running expiry code")
