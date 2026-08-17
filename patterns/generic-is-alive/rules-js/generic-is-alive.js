rules.JSRule({
  name: "A sensor stopped reporting",
  triggers: [triggers.GroupStateChangeTrigger("DeviceStatuses", undefined, "UNDEF")],
  execute: (event) => {
    // Meldung oder Alarm ausloesen
  }
});
