const alertTimers = {};

function alertTimerExpired(itemName, name, origState) {
  delete alertTimers[itemName];
  if (items.getItem(itemName).state === origState) {
    const displayValue = actions.Transformation.transform("MAP", "admin.map", String(items.getItem(itemName).state));
    console.log(name + " is now " + displayValue);

    const meta = items.getItem(itemName).getMetadata("Alert");
    if (!meta || meta.configuration.alerted !== "ON") {
      items.getItem(itemName).replaceMetadata("Alert", "alerted", { alerted: "ON" });
    }
  }
}

rules.JSRule({
  name: "Device online/offline",
  description: "Track device online/offline status",
  tags: ["admin"],
  triggers: [triggers.GroupStateChangeTrigger("gSensorStatus")],
  execute: (event) => {
    if (event.oldState === undefined || event.oldState === null) return;

    const itemName = event.itemName;
    const meta = items.getItem(itemName).getMetadata("Alert");
    const alerted = (meta && meta.configuration.alerted) || "OFF";
    const nameMeta = items.getItem(itemName).getMetadata();
    const name = (nameMeta && nameMeta.value) || itemName;

    if (alertTimers[itemName]) {
      clearTimeout(alertTimers[itemName]);
      delete alertTimers[itemName];
      return; // Flapping erkannt: laufenden Timer abbrechen, kein neuer Alert
    }

    if (alerted === String(event.newState)) {
      alertTimers[itemName] = setTimeout(
        () => alertTimerExpired(itemName, name, event.newState),
        60000
      );
    }
  }
});
