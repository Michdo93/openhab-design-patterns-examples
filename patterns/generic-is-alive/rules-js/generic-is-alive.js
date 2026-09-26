rules.JSRule({
  name: "A sensor stopped reporting",
  triggers: [triggers.GroupStateChangeTrigger("DeviceStatuses", undefined, "UNDEF")],
  execute: (event) => {
    // Meldung oder Alarm auslösen
    console.warn(event.itemName + " stopped reporting (UNDEF) - raise alert/notification");
  }
});
