rules.JSRule({
  name: "Find associated item via naming convention",
  triggers: [triggers.GroupStateChangeTrigger("gSensors")],
  execute: (event) => {
    if (event.itemName.endsWith("_Status")) {
      return;
    }
    const statusItem = items.getItem(event.itemName + "_Status");
    statusItem.postUpdate("ON");
  }
});
