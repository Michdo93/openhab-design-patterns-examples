rules.JSRule({
  name: "Toggle Lampe mit Feedback",
  triggers: [triggers.ItemCommandTrigger("mqttSwitchIn2", "OFF")],
  execute: (event) => {
    const lamp = items.getItem("modbusSwitchOut1");
    if (lamp.state !== "ON") {
      lamp.sendCommand("ON");
    } else {
      lamp.sendCommand("OFF");
    }
    lamp.postUpdate(lamp.state);
  }
});
