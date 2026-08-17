from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger, ItemStateChangeTrigger


def build_triggers_from_metadata():
    # Beispiel: alle Items mit dem Metadaten-Namespace "triggerRule" einsammeln
    triggers = []
    for item in Registry.getItems():
        if item.getMetadata().get("triggerRule") is not None:
            triggers.append(ItemStateChangeTrigger(item.name))
    return triggers


@rule(name="Dynamische Metadaten-Regel")
class DynamischeMetadatenRegel:
    def buildTriggers(self):
        found = build_triggers_from_metadata()
        if not found:
            self.logger.warn("Keine passenden Items gefunden")
        return found

    def execute(self, module, input):
        self.logger.info(str(input.get("itemName")) + " hat sich geaendert (dynamischer Trigger)")


@rule(triggers=[ItemCommandTrigger("Reload_Item", "ON")])
class ReloadDynamischeRegel:
    def execute(self, module, input):
        # Ein erneuter Aufruf von buildTriggers() erfolgt automatisch,
        # sobald das Skript neu geladen wird (z. B. durch Speichern der Datei).
        self.logger.info("Trigger werden beim naechsten Neuladen des Skripts aktualisiert")
