rules.JSRule({
  name: "Enable/Disable example rule",
  triggers: [triggers.ItemStateChangeTrigger("exampleRule")],
  execute: (event) => {
    rules.setEnabled("example_rule_uid", items.getItem("exampleRule").state === "ON");
  }
});
