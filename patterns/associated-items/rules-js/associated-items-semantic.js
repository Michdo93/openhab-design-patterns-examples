rules.JSRule({
  name: "Sensor hat ein Update",
  triggers: [triggers.ItemStateChangeTrigger("SomeSensor")],
  execute: (event) => {
    const equipment = actions.Semantics.getEquipment(items.getItem(event.itemName));
    if (!equipment) {
      console.warn("Kein Equipment fuer SomeSensor gefunden");
      return;
    }

    // equipment.members ist ein rohes Java-Set (equipment kommt aus einer
    // Java-Action, nicht aus dem JS-Wrapper) - erst in echte JS-Items
    // umwandeln, damit JS-Array-Methoden wie .find()/.includes() nutzbar sind.
    const members = Array.from(equipment.members).map((i) => items.getItem(i.name));

    // Ansatz: Equipment-Name (nur als Beispiel, nicht robust: setzt voraus,
    // dass ein Item exakt "<Equipmentname>_Status" existiert)
    // const byName = items.getItem(equipment.name + "_Status");

    // Ansatz: Item-Typ
    const byType = members.find((i) => i.type === "Switch");

    // Ansatz: Item-Tag
    const byTag = members.find((i) => i.tags.includes("Status"));

    // Ansatz: mehrere Kriterien (robust, unabhaengig vom Equipment-Namen)
    const byMulti = members.find(
      (i) => i.tags.includes("Status") && i.name.endsWith("_Status")
    );

    if (!byMulti) {
      console.warn("Kein Status-Item im Equipment " + equipment.name + " gefunden");
      return;
    }
    byMulti.postUpdate(items.getItem(event.itemName).state);
  }
});
