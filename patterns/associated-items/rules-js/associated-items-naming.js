rules.JSRule({
  name: "Zugehoeriges Item ueber Namenskonvention finden",
  triggers: [triggers.GroupStateChangeTrigger("gSensors")],
  execute: (event) => {
    const statusItem = items.getItem(event.itemName + "_Status");
    statusItem.postUpdate("ON");
  }
});
