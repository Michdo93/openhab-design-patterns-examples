rules.JSRule({
  name: "Heizung mit Hysterese",
  triggers: [triggers.ItemStateChangeTrigger("MyTemp")],
  execute: (event) => {
    const temp = parseFloat(items.getItem("MyTemp").state);
    let newCommand = "STAY";

    if (temp < 68) {
      newCommand = "ON";
    } else if (temp >= 70) {
      newCommand = "OFF";
    }

    if (newCommand !== "STAY" && newCommand !== items.getItem("MyHeater").state) {
      items.getItem("MyHeater").sendCommand(newCommand);
    }
  }
});
