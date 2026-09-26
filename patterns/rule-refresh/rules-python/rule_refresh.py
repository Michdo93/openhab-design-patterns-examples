from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger, ItemStateChangeTrigger


def build_triggers_from_metadata():
    # Beispiel: alle Items mit dem Metadaten-Namespace "triggerRule" einsammeln
    triggers = []
    for item in Registry.getItems():
        if item.getMetadata().get("triggerRule") is not None:
            triggers.append(ItemStateChangeTrigger(item.getName()))
    return triggers


@rule(name="Dynamic metadata rule")
class DynamicMetadataRule:
    def buildTriggers(self):
        found = build_triggers_from_metadata()
        if not found:
            self.logger.warn("No matching items found")
        return found

    def execute(self, module, input):
        event = input.get("event")
        item_name = event.getItemName() if event else "unknown"
        self.logger.info(item_name + " changed (dynamic trigger)")


@rule(triggers=[ItemCommandTrigger("Reload_Item", "ON")])
class ReloadDynamicRule:
    def execute(self, module, input):
        # Ein erneuter Aufruf von buildTriggers() erfolgt automatisch,
        # sobald das Skript neu geladen wird (z. B. durch Speichern der Datei).
        self.logger.info("Triggers will be updated on the next script reload")
