rules.JSRule({
  name: "Start Zone 1 Watering",
  triggers: [triggers.ItemStateChangeTrigger("SomeCondition", undefined, "ON")],
  execute: (event) => {
    items.getItem("VT_Watering_Zone1").postUpdate("START");
  }
});
