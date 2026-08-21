rules.JSRule({
  name: "Sensor hat ein Update",
  triggers: [triggers.ItemStateChangeTrigger("SomeSensor")],
  execute: (event) => {
    const equipment = actions.Semantics.getEquipment(items.getItem(event.itemName));
    if (!equipment) {
      console.warn("Kein Equipment fuer SomeSensor gefunden");
      return;
    }

    // Ansatz: Equipment-Name (nur als Beispiel, nicht robust: setzt voraus,
    // dass ein Item exakt "<Equipmentname>_Status" existiert)
    // const byName = items.getItem(equipment.name + "_Status");

    // Ansatz: Item-Typ
    const byType = equipment.members.find((i) => i.type === "Switch");

    // Ansatz: Item-Tag
    const byTag = equipment.members.find((i) => i.tags.includes("Status"));

    // Ansatz: mehrere Kriterien (robust, unabhaengig vom Equipment-Namen)
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
