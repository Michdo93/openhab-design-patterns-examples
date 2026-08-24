rules.JSRule({
  name: "Sensor hat ein Update",
  triggers: [triggers.ItemStateChangeTrigger("SomeSensor")],
  execute: (event) => {
    const equipment = actions.Semantics.getEquipment(items.getItem(event.itemName));
    if (!equipment) {
      console.warn("Kein Equipment fuer SomeSensor gefunden");
      return;
    }

    const byMulti = equipment.members.find(
      (i) => i.tags.includes("Status") && i.name.endsWith("_Status")
    );

    if (!byMulti) {
      console.warn("Kein Status-Item im Equipment " + equipment.name + " gefunden");
      return;
    }
    byMulti.postUpdate(items.getItem(event.itemName).state);
  }
});
