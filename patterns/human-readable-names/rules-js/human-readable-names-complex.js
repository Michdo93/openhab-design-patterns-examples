const alertTimers = new Map();

rules.JSRule({
  name: "Status Alert",
  triggers: [triggers.GroupStateChangeTrigger("gSensorStatus")],
  execute: (event) => {
    if (event.oldState === undefined || event.oldState === null) return;

    const itemName = event.itemName;
    if (alertTimers.has(itemName)) alertTimers.get(itemName).cancel();

    const origState = String(items.getItem(itemName).state);

    const t = actions.ScriptExecution.createTimer(
      time.ZonedDateTime.now().plusMinutes(1),
      () => {
        alertTimers.delete(itemName);
        if (String(items.getItem(itemName).state) === origState) {
          const name = actions.Transformation.transform("MAP", "admin.map", itemName) || itemName;
          const stateName = actions.Transformation.transform("MAP", "admin.map", origState) || origState;

          console.log(name + " ist jetzt " + stateName);
          items.getItem(itemName + "_Alerted").postUpdate("ON");
        }
      }
    );
    alertTimers.set(itemName, t);
  }
});
