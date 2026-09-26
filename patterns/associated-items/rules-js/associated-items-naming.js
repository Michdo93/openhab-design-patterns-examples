rules.JSRule({
  name: "Zugehöriges Item über Namenskonvention finden",
  triggers: [triggers.GroupStateChangeTrigger("gSensors")],
  execute: (event) => {
    if (event.itemName.endsWith("_Status")) {
      return;
    }
    const statusItem = items.getItem(event.itemName + "_Status");
    statusItem.postUpdate("ON");
  }
});
