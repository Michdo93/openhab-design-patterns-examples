rules.JSRule({
  name: "Light control received command",
  triggers: [triggers.GroupCommandTrigger("LightControls")],
  execute: (event) => {
    const parts = event.itemName.split("_");
    const lightName = parts[0];
    const source = parts[1];
    const command = event.receivedCommand;

    if (source === "Proxy") return; // Proxy sollte nie direkt befehligt werden

    const proxy = items.getItem(lightName + "_Proxy");
    const device = items.getItem(lightName + "_Device");
    const ui = items.getItem(lightName + "_UI");
    const rulesItem = items.getItem(lightName + "_Rules");

    if (proxy.state !== command) proxy.postUpdate(command);
    if (ui.state !== command) ui.postUpdate(command);
    if (rulesItem.state !== command) rulesItem.postUpdate(command);
    if (device.state !== command) device.sendCommand(command);

    console.log("Quelle=" + source + " -> " + lightName + " = " + command);
  }
});
