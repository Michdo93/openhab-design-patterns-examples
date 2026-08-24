rules.JSRule({
  name: "A sensor stopped reporting",
  triggers: [triggers.GroupStateChangeTrigger("DeviceStatuses", undefined, "UNDEF")],
  execute: (event) => {
    // Meldung oder Alarm ausloesen
    console.warn(event.itemName + " meldet sich nicht mehr (UNDEF) - Alarm/Meldung ausloesen");
  }
});
