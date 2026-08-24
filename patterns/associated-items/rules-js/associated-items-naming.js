const { rules, triggers, items } = require('openhab');

rules.JSRule({
  name: "Zugehoeriges Item ueber Namenskonvention finden",
  triggers: [triggers.ItemStateChangeTrigger("gSensors")],
  execute: (event) => {
    if (event.itemName.endsWith("_Status")) {
      return;
    }
    const statusItem = items.getItem(event.itemName + "_Status");
    statusItem.postUpdate("ON");
  }
});
