from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger


@rule()
class EineRegelDieDenTimerStartet:
    def buildTriggers(self):
        return []  # irgendein Trigger

    def execute(self, module, input):
        # Arbeitsschritte ausfuehren

        if str(Registry.getItem("MyTimer").state) == "ON":
            pass  # Aktion, falls Timer aktiv ist

        # Timer abbrechen
        Registry.getItem("MyTimer").postUpdate("OFF")

        # Timer starten
        Registry.getItem("MyTimer").sendCommand("ON")


@rule(triggers=[ItemCommandTrigger("MyTimer", "OFF")])
class MyTimerAbgelaufen:
    def execute(self, module, input):
        pass  # Code, der nach Ablauf ausgefuehrt werden soll
