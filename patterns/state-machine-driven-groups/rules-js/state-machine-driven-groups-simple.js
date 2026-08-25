rules.JSRule({
  name: "Set lights based on Time of Day",
  triggers: [triggers.ItemStateChangeTrigger("vTimeOfDay")],
  execute: (event) => {
    const timeOfDay = items.getItem("vTimeOfDay").state;
    items.getItem("gLights_OFF_" + timeOfDay).sendCommand("OFF");
    items.getItem("gLights_ON_" + timeOfDay).sendCommand("ON");
    console.log("vTimeOfDay=" + timeOfDay + " -> Lichtgruppen angesteuert");
  }
});
