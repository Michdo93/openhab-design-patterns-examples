let debounceTimer = null;

rules.JSRule({
  name: "Debounced Motion Sensor",
  triggers: [triggers.ItemStateChangeTrigger("motionSensor")],
  execute: (event) => {
    if (debounceTimer === null) {
      console.log("Motion detected - turning light on");
      items.getItem("light").sendCommand("ON");

      debounceTimer = actions.ScriptExecution.createTimer(
        time.ZonedDateTime.now().plusSeconds(2),
        () => {
          debounceTimer = null;
          console.log("Debounce finished - new events possible");
        }
      );
    } else {
      console.log("Event ignored - timer still running");
    }
  }
});
