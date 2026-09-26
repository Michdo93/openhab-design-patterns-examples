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
    console.warn("No matching items found, rule not created");
    return;
  }

  rules.JSRule({
    id: DYNAMIC_RULE_ID,
    name: "Dynamic metadata rule",
    triggers: dynamicTriggers,
    overwrite: true,
    execute: (event) => {
      console.log(event.itemName + " changed (dynamic trigger)");
    }
  });
}

rules.JSRule({
  name: "Reload dynamic rule",
  triggers: [triggers.ItemCommandTrigger("Reload_Item", "ON")],
  execute: (event) => {
    createDynamicRule();
  }
});

// Beim ersten Laden des Skripts einmal ausführen
createDynamicRule();
