rules.JSRule({
  name: "Enable/Disable example rule",
  triggers: [triggers.ItemStateChangeTrigger("exampleRule")],
  execute: (event) => {
    const enable = items.getItem("exampleRule").state === "ON";
    try {
      rules.setEnabled("example_rule_uid", enable);
      console.log("example_rule_uid -> enabled=" + enable);
    } catch (e) {
      console.warn("Could not toggle example_rule_uid: " + e.message);
    }
  }
});
