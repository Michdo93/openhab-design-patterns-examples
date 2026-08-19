from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger


@rule(triggers=[ItemCommandTrigger("StartMyTimerTrigger", "ON")])
class EineRegelDieDenTimerStartet:
    def execute(self, module, input):
        # Arbeitsschritte ausfuehren

        if str(Registry.getItem("MyTimer").getState()) == "ON":
            self.logger.info("Timer ist bereits aktiv - wird neu gestartet")

        # Timer abbrechen
        Registry.getItem("MyTimer").postUpdate("OFF")

        # Timer starten
        Registry.getItem("MyTimer").sendCommand("ON")
        self.logger.info("MyTimer gestartet (5 Minuten)")


@rule(triggers=[ItemCommandTrigger("MyTimer", "OFF")])
class MyTimerAbgelaufen:
    def execute(self, module, input):
        self.logger.info("MyTimer abgelaufen - Code nach Ablauf wird ausgefuehrt")
