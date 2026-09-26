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
    // Aktionen ausführen
    items.getItem("WatchedItem1").sendCommand("ON");
    items.getItem("DeadMansSwitch").sendCommand("MANUAL");
  }
});

rules.JSRule({
  name: "Is Manually Triggered?",
  triggers: [triggers.GroupStateUpdateTrigger("gWatchItems")],
  execute: (event) => {
    if (items.getItem("DeadMansSwitch").state === "MANUAL") {
      console.log("Item was triggered manually");
    } else {
      console.log("Item was triggered by a rule (DeadMansSwitch=RULE)");
    }
  }
});
