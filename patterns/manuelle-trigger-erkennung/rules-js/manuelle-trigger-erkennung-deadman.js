rules.JSRule({
  name: "System Started",
  triggers: [triggers.SystemStartlevelTrigger(100)],
  execute: (event) => {
    items.getItem("DeadMansSwitch").sendCommand("STARTUP");
  }
});

rules.JSRule({
  name: "Rule that changes a gWatchItem",
  triggers: [ /* Trigger */ ],
  execute: (event) => {
    items.getItem("DeadMansSwitch").sendCommand("RULE");
    // Aktionen ausfuehren
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
