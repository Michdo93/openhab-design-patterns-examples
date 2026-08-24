const { rules, triggers, items, actions } = require('openhab');

rules.JSRule({
  name: "Sensor hat ein Update",
  triggers: [triggers.ItemStateChangeTrigger("SomeSensor")], //[cite: 1]
  execute: (event) => {
    const equipment = actions.Semantics.getEquipment(items.getItem(event.itemName)); //[cite: 1]
    if (!equipment) {
      console.warn("Kein Equipment fuer SomeSensor gefunden"); //[cite: 1]
      return;
    }

    const byMulti = equipment.members.find( //[cite: 1]
      (i) => i.tags.includes("Status") && i.name.endsWith("_Status") //[cite: 1]
    );

    if (!byMulti) {
      console.warn("Kein Status-Item im Equipment " + equipment.name + " gefunden"); //[cite: 1]
      return;
    }
    byMulti.postUpdate(items.getItem(event.itemName).state); //[cite: 1]
  }
});
