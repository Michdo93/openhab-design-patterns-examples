let timer = null;

rules.JSRule({
  name: "Debounce Person1",
  triggers: [triggers.ItemStateChangeTrigger("Person1PresenceSensor")],
  execute: (event) => {
    if (timer !== null) timer.cancel();
    timer = actions.ScriptExecution.createTimer(
      time.ZonedDateTime.now().plusMinutes(2),
      () => {
        const sensor = items.getItem("Person1PresenceSensor").state;
        if (items.getItem("Person1Presence").state !== sensor) {
          items.getItem("Person1Presence").postUpdate(sensor);
        }
        timer = null;
      }
    );
  }
});
