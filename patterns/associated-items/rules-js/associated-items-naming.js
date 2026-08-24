const { rules, triggers, items } = require('openhab');

rules.JSRule({
  name: "Zugehoeriges Item ueber Namenskonvention finden",
  triggers: [triggers.ItemGroupStateChangeTrigger("gSensors")], // Angepasst
  execute: (event) => {
    if (event.itemName.endsWith("_Status")) { //[cite: 2]
      return;
    }
    const statusItem = items.getItem(event.itemName + "_Status"); //[cite: 2]
    statusItem.postUpdate("ON"); //[cite: 2]
  }
});
