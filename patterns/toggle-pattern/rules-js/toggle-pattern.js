rules.JSRule({
  name: "Toggle Lampe",
  triggers: [triggers.ItemCommandTrigger("mqttSwitchIn2", "OFF")],
  execute: (event) => {
    if (items.getItem("modbusSwitchOut1").state !== "ON") {
      items.getItem("modbusSwitchOut1").sendCommand("ON");
    } else {
      items.getItem("modbusSwitchOut1").sendCommand("OFF");
    }
  }
});
