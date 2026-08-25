rules.JSRule({
  name: "Example rule",
  id: "example_rule_uid",
  triggers: [triggers.ItemCommandTrigger("DummyExecTrigger")],
  execute: (event) => {
    items.getItem("isRunningExampleRule").sendCommand("ON");

    if (items.getItem("isRunningExampleRule").state === "ON") {
      // Teil 1 der Regel
    } else {
      // Aenderungen rueckgaengig machen
    }

    if (items.getItem("isRunningExampleRule").state === "ON") {
      // Teil 2 der Regel
    } else {
      // Aenderungen rueckgaengig machen
    }

    items.getItem("isRunningExampleRule").sendCommand("OFF");
  }
});
