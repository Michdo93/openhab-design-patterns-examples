rules.JSRule({
  name: "System Started",
  triggers: [triggers.SystemStartlevelTrigger(100)],
  execute: (event) => {
    items.getItem("DeadMansSwitch").sendCommand("STARTUP");
  }
});

rules.JSRule({
  name: "Rule that changes a gWatchItem",
  triggers: [triggers.ItemCommandTrigger("SomeRuleTrigger", "ON")],
  execute: (event) => {
    items.getItem("DeadMansSwitch").sendCommand("RULE");
    // Aktionen ausfuehren
    items.getItem("WatchedItem1").sendCommand("ON");
    items.getItem("DeadMansSwitch").sendCommand("MANUAL");
  }
});

rules.JSRule({
  name: "Is Manually Triggered?",
  triggers: [triggers.GroupStateUpdateTrigger("gWatchItems")],
  execute: (event) => {
    if (items.getItem("DeadMansSwitch").state === "MANUAL") {
      // Element wurde manuell ausgeloest
    }
  }
});
