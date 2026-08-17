const supervisionTimers = new Map();
const T_RB_SECONDS = 30;

rules.JSRule({
  name: "MQTT State Supervision",
  triggers: [triggers.ItemCommandTrigger("MySwitch")],
  execute: (event) => {
    const expectedState = String(event.receivedCommand);
    const itemName = event.itemName;

    if (supervisionTimers.has(itemName)) {
      supervisionTimers.get(itemName).cancel();
    }

    const t = actions.ScriptExecution.createTimer(
      time.ZonedDateTime.now().plusSeconds(T_RB_SECONDS),
      () => {
        console.warn(itemName + " hat den Zustand " + expectedState + " nicht erreicht");
        // z. B. Benachrichtigung senden
        supervisionTimers.delete(itemName);
      }
    );
    supervisionTimers.set(itemName, t);
  }
});

rules.JSRule({
  name: "MQTT State Update",
  triggers: [triggers.ItemStateChangeTrigger("MySwitch")],
  execute: (event) => {
    if (supervisionTimers.has(event.itemName)) {
      supervisionTimers.get(event.itemName).cancel();
      supervisionTimers.delete(event.itemName);
    }
  }
});
