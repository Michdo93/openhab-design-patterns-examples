const timers = new Map();

rules.JSRule({
  name: "Presence detection debounce",
  triggers: [
    triggers.ItemStateChangeTrigger("Person1_PresenceSensors"),
    triggers.ItemStateChangeTrigger("Person2_PresenceSensors")
  ],
  execute: (event) => {
    const triggeringItem = items.getItem(event.itemName);

    if (timers.has(triggeringItem.name)) {
      timers.get(triggeringItem.name).cancel();
    }

    const delay = triggeringItem.state === "ON" ? 0 : 2;
    const t = actions.ScriptExecution.createTimer(
      time.ZonedDateTime.now().plusMinutes(delay),
      () => {
        const proxyName = triggeringItem.name.split("_")[0] + "_Present";
        const proxyItem = items.getItem(proxyName);
        if (proxyItem.state !== triggeringItem.state) {
          proxyItem.sendCommand(triggeringItem.state);
        }
        timers.delete(triggeringItem.name);
      }
    );
    timers.set(triggeringItem.name, t);
  }
});
