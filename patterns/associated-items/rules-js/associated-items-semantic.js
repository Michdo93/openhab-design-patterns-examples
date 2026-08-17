rules.JSRule({
  name: "Sensor hat ein Update",
  triggers: [triggers.ItemStateChangeTrigger("SomeSensor")],
  execute: (event) => {
    const equipment = actions.Semantics.getEquipment(items.getItem(event.itemName));

    // Ansatz: Equipment-Name
    const byName = items.getItem(equipment.name + "_Status");

    // Ansatz: Item-Typ
    const byType = equipment.members.find((i) => i.type === "Switch");

    // Ansatz: Item-Tag
    const byTag = equipment.members.find((i) => i.tags.includes("Status"));

    // Ansatz: mehrere Kriterien
    const byMulti = equipment.members.find(
      (i) => i.tags.includes("Status") && i.name.endsWith("_Status")
    );

    byName.postUpdate(items.getItem(event.itemName).state);
  }
});
