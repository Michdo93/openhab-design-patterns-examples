const timers = new Map();

rules.JSRule({
  name: "Alert if door open for over 60 minutes",
  triggers: [triggers.GroupStateChangeTrigger("Doors")],
  execute: (event) => {
    const itemName = event.itemName;

    // Bestehenden Timer abbrechen
    if (timers.has(itemName)) {
      timers.get(itemName).cancel();
      timers.delete(itemName);
    }

    // Timer neu erstellen, wenn Tuer geoeffnet wurde
    if (items.getItem(itemName).state === "OPEN") {
      const t = actions.ScriptExecution.createTimer(
        time.ZonedDateTime.now().plusMinutes(60),
        () => {
          items.getItem("Alert").sendCommand(itemName + " is still open!");
        }
      );
      timers.set(itemName, t);
    }
  }
});
