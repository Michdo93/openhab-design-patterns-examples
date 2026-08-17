rules.JSRule({
  name: "Ceiling fan control",
  triggers: [triggers.ItemStateChangeTrigger("MotionSensor", undefined, "ON")],
  execute: (event) => {
    if (items.getItem("CeilingFanTimer").state !== "ON") {
      items.getItem("CeilingFanTimer").sendCommand("OFF"); // Timer starten
    }
  }
});

rules.JSRule({
  name: "Ceiling fan loop",
  triggers: [triggers.ItemCommandTrigger("CeilingFanTimer", "OFF")],
  execute: (event) => {
    if (items.getItem("vTimeOfDay").state !== "NIGHT") return;

    let newState = "STAY";
    const current = parseFloat(items.getItem("CurrentTemp").state);
    const target = parseFloat(items.getItem("TargetTemp").state);
    if (current > target) newState = "ON";
    else if (current < target - 1) newState = "OFF";

    if (newState !== "STAY" && items.getItem("Fan").state !== newState) {
      items.getItem("Fan").sendCommand(newState);
    }

    items.getItem("CeilingFanTimer").sendCommand("ON");
  }
});
