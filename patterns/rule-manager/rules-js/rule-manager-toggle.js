rules.JSRule({
  name: "Enable/Disable example rule",
  triggers: [triggers.ItemStateChangeTrigger("exampleRule")],
  execute: (event) => {
    const enable = items.getItem("exampleRule").state === "ON";
    try {
      rules.setEnabled("example_rule_uid", enable);
      console.log("example_rule_uid -> enabled=" + enable);
    } catch (e) {
      console.warn("Konnte example_rule_uid nicht umschalten: " + e.message);
    }
  }
});
