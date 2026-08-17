const DYNAMIC_RULE_ID = "dynamic_metadata_rule";

function buildTriggersFromMetadata() {
  // Beispiel: alle Items mit dem Metadaten-Namespace "triggerRule" einsammeln
  return items.getItems()
    .filter((i) => i.getMetadata("triggerRule") !== null)
    .map((i) => triggers.ItemStateChangeTrigger(i.name));
}

function createDynamicRule() {
  const dynamicTriggers = buildTriggersFromMetadata();
  if (dynamicTriggers.length === 0) {
    console.warn("Keine passenden Items gefunden, Regel wird nicht erstellt");
    return;
  }

  rules.JSRule({
    id: DYNAMIC_RULE_ID,
    name: "Dynamische Metadaten-Regel",
    triggers: dynamicTriggers,
    overwrite: true,
    execute: (event) => {
      console.log(event.itemName + " hat sich geaendert (dynamischer Trigger)");
    }
  });
}

rules.JSRule({
  name: "Reload dynamische Regel",
  triggers: [triggers.ItemCommandTrigger("Reload_Item", "ON")],
  execute: (event) => {
    createDynamicRule();
  }
});

// Beim ersten Laden des Skripts einmal ausfuehren
createDynamicRule();
