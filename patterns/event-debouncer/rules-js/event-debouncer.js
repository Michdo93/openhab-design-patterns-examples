let debounceTimer = null;

rules.JSRule({
  name: "Debounced Motion Sensor",
  triggers: [triggers.ItemStateChangeTrigger("motionSensor")],
  execute: (event) => {
    if (debounceTimer === null) {
      console.log("Bewegung erkannt - Licht einschalten");
      items.getItem("light").sendCommand("ON");

      debounceTimer = actions.ScriptExecution.createTimer(
        time.ZonedDateTime.now().plusSeconds(2),
        () => {
          debounceTimer = null;
          console.log("Debounce beendet - neue Events moeglich");
        }
      );
    } else {
      console.log("Event ignoriert - Timer laeuft noch");
    }
  }
});
