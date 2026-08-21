let timer = null;

rules.JSRule({
  name: "Debounce Person1",
  triggers: [triggers.ItemStateChangeTrigger("Person1PresenceSensor")],
  execute: (event) => {
    if (timer !== null) timer.cancel();

    const sensorState = items.getItem("Person1PresenceSensor").state;
    const delaySeconds = sensorState === "ON" ? 0 : 120;

    timer = actions.ScriptExecution.createTimer(
      time.ZonedDateTime.now().plusSeconds(delaySeconds),
      () => {
        if (items.getItem("Person1Presence").state !== sensorState) {
          items.getItem("Person1Presence").postUpdate(sensorState);
          console.log("Person1Presence uebernimmt " + sensorState + " (Verzoegerung=" + delaySeconds + "s)");
        }
        timer = null;
      }
    );
  }
});
